"""Inicia, supervisa y cancela los procesos hijos de los trabajos."""

import logging
import subprocess
import threading
from collections.abc import Callable
from datetime import datetime, timezone

from .models import Job, JobStatus


logger = logging.getLogger("JobExecutor")
# El runner entrega esta función para que el executor avise cuando termina un hijo.
CompletionCallback = Callable[[Job], None]


class JobExecutor:
    """Inicia procesos hijos y recoge sus resultados sin bloquear la CLI.

    JobRunner llama a `execute`; cada proceso se supervisa en un hilo y,
    al finalizar, el callback permite al runner iniciar el siguiente trabajo.
    """

    def __init__(self) -> None:
        # Relaciona cada ID de trabajo con su proceso mientras está activo.
        self.processes: dict[str, subprocess.Popen[str]] = {}
        # Protege el registro de procesos frente al hilo monitor y al hilo CLI.
        self._lock = threading.Lock()

    def execute(
        self,
        job: Job,
        on_complete: CompletionCallback | None = None,
    ) -> bool:
        """Inicia el proceso hijo y devuelve si el lanzamiento tuvo éxito."""
        try:
            # Se pasa una lista de argumentos y no se invoca un shell del sistema.
            process = subprocess.Popen(
                job.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        except OSError as error:
            # Si el ejecutable no existe, el trabajo falla antes de tener PID.
            job.status = JobStatus.FAILED
            job.error_message = str(error)
            job.finished_at = datetime.now(timezone.utc).isoformat()
            logger.error("No se pudo iniciar el trabajo %s: %s", job.id, error)
            return False

        job.pid = process.pid
        job.started_at = datetime.now(timezone.utc).isoformat()
        job.status = JobStatus.RUNNING

        # Registrar el proceso permite a cancel() localizarlo usando el ID del job.
        with self._lock:
            self.processes[job.id] = process

        # communicate() espera al hijo en este hilo aparte, dejando libre la CLI.
        monitor = threading.Thread(
            target=self._monitor_process,
            args=(job, process, on_complete),
            name=f"beanrunner-job-{job.id}",
            daemon=True,
        )
        monitor.start()
        return True

    def cancel(self, job: Job, grace_seconds: float = 1.0) -> tuple[bool, str]:
        """Termina el hijo y fuerza su cierre si no responde en el plazo dado."""
        with self._lock:
            # El ID conecta el objeto Job con el Popen creado por execute().
            process = self.processes.get(job.id)
            if process is None or process.poll() is not None:
                return False, "El proceso ya terminó o no está activo."

            # El monitor usa esta marca para diferenciar cancelación de fallo.
            job.cancel_requested = True
            try:
                process.terminate()
            except OSError as error:
                job.cancel_requested = False
                logger.error("No se pudo terminar el trabajo %s: %s", job.id, error)
                return False, f"No se pudo terminar el proceso: {error}"

        # Se da tiempo para terminar normalmente antes de forzar la terminación.
        try:
            process.wait(timeout=grace_seconds)
        except subprocess.TimeoutExpired:
            logger.warning(
                "El trabajo %s ignoró SIGTERM; se enviará terminación forzada.",
                job.id,
            )
            process.kill()
            process.wait()

        return True, "Se solicitó la terminación del proceso."

    def get_process(self, job_id: str) -> subprocess.Popen[str] | None:
        """Devuelve el proceso registrado para ese trabajo, si sigue activo."""
        with self._lock:
            return self.processes.get(job_id)

    @property
    def active_count(self) -> int:
        """Cuenta los procesos hijos que todavía están bajo supervisión."""
        with self._lock:
            return len(self.processes)

    def _monitor_process(
        self,
        job: Job,
        process: subprocess.Popen[str],
        on_complete: CompletionCallback | None,
    ) -> None:
        """Espera al hijo, recoge su salida y actualiza el estado del trabajo."""
        try:
            # communicate espera el fin y recoge ambas salidas para evitar mezclarlas.
            stdout, stderr = process.communicate()
            # El resultado capturado se guarda en el Job que consultan runner y CLI.
            job.stdout = stdout
            job.stderr = stderr
            job.exit_code = process.returncode
            job.finished_at = datetime.now(timezone.utc).isoformat()

            if job.cancel_requested:
                job.status = JobStatus.CANCELED
            elif process.returncode == 0:
                job.status = JobStatus.SUCCEEDED
            else:
                job.status = JobStatus.FAILED
        except OSError as error:
            job.status = JobStatus.FAILED
            job.error_message = str(error)
            job.finished_at = datetime.now(timezone.utc).isoformat()
            logger.exception("Falló la recolección del resultado del trabajo %s", job.id)
        finally:
            # Al retirar el proceso se libera un slot; el callback permite llenar la cola.
            with self._lock:
                self.processes.pop(job.id, None)
            if on_complete is not None:
                on_complete(job)
