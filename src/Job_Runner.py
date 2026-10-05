"""Coordina el envío, la ejecución y la consulta de trabajos locales."""

import threading
from collections import deque
from datetime import datetime, timezone

from .executor import JobExecutor
from .manager import JobManager
from .models import Job, JobStatus
from .submitter import JobSubmitter, RawCommand


class JobRunner:
    """Coordina los componentes que participan en el ciclo de vida de un trabajo.

    `JobRunner` es la fachada que usa la CLI: recibe solicitudes, conserva los
    trabajos, los pone en cola y conecta al ejecutor con el gestor.
    """

    def __init__(self, max_concurrency: int = 3) -> None:
        if max_concurrency < 1:
            raise ValueError("max_concurrency debe ser al menos 1.")

        # Almacenamiento compartido: submitter crea trabajos y manager los consulta.
        self.jobs: dict[str, Job] = {}
        # La cola guarda IDs, no copias de Job; el orden es FIFO.
        self.queue: deque[str] = deque()
        # Límite de procesos hijos que pueden ejecutarse simultáneamente.
        self.max_concurrency = max_concurrency
        # El mismo lock coordina cambios en trabajos, cola y operaciones del manager.
        self._lock = threading.RLock()
        # Impide iniciar trabajos nuevos cuando shutdown ya comenzó.
        self._shutting_down = False

        # Los tres componentes colaboran sobre los mismos trabajos:
        # submitter valida/crea, executor ejecuta y manager consulta/cancela.
        self.submitter = JobSubmitter(self.jobs)
        self.executor = JobExecutor()
        self.manager = JobManager(self.jobs, self.executor, self._lock)

    def submit_job(self, command: RawCommand) -> Job:
        """Valida, registra, encola e inicia si hay capacidad disponible."""
        with self._lock:
            # El submitter solo registra; el runner decide cuándo ejecutarlo.
            # El ID retornado aquí no se necesita: está disponible en job.id.
            _, job = self.submitter.submit_job(command)
            self.queue.append(job.id)
            self._start_queued_jobs()
            return job

    def execute_job(self, job_id: str) -> Job | None:
        """Intenta iniciar trabajos en cola; se conserva por compatibilidad."""
        with self._lock:
            job = self.jobs.get(job_id)
            if job is None:
                return None
            self._start_queued_jobs()
            return job

    def get_job(self, job_id: str) -> Job | None:
        """Devuelve los metadatos o None si el ID no está registrado."""
        # La búsqueda concreta vive en manager, que comparte el registro jobs.
        return self.manager.get_job(job_id)

    def get_status(self, job_id: str) -> JobStatus | None:
        """Devuelve el estado actual o None si no existe ese ID."""
        job = self.get_job(job_id)
        return job.status if job is not None else None

    def list_jobs(self, status_filter: JobStatus | None = None) -> list[Job]:
        """Lista los trabajos registrados, opcionalmente filtrados por estado."""
        return self.manager.list_jobs(status_filter)

    def cancel_job(self, job_id: str) -> tuple[bool, str]:
        """Cancela un trabajo en cola o solicita detener su proceso hijo."""
        with self._lock:
            # manager cambia el estado o llama al executor; después se repone la cola.
            result = self.manager.cancel_job(job_id)
            self._start_queued_jobs()
            return result

    def shutdown(self) -> None:
        """Evita nuevos inicios, cancela la cola y termina procesos activos."""
        with self._lock:
            self._shutting_down = True
            # Lo pendiente no debe empezar durante el cierre: se marca cancelado.
            for job_id in tuple(self.queue):
                job = self.jobs.get(job_id)
                if job is not None and job.status == JobStatus.QUEUED:
                    job.status = JobStatus.CANCELED
                    job.finished_at = datetime.now(timezone.utc).isoformat()
            self.queue.clear()

            # Copiamos los trabajos activos para cancelarlos fuera del lock.
            running_jobs = [
                job for job in self.jobs.values() if job.status == JobStatus.RUNNING
            ]

        for job in running_jobs:
            self.manager.cancel_job(job.id)

    def _start_queued_jobs(self) -> None:
        """Ocupa los espacios libres respetando el orden FIFO de la cola."""
        if self._shutting_down:
            return
        # Cada ejecución libera un slot; el callback vuelve a llenar ese espacio.
        while self.queue and self.executor.active_count < self.max_concurrency:
            job_id = self.queue.popleft()
            job = self.jobs.get(job_id)
            if job is None or job.status != JobStatus.QUEUED:
                continue
            self.executor.execute(job, self._on_job_finished)

    def _on_job_finished(self, _job: Job) -> None:
        """Reanuda la cola cuando el ejecutor termina de supervisar un trabajo."""
        with self._lock:
            self._start_queued_jobs()
