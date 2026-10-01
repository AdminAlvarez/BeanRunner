"""
GESTIÓN Y CONTROL DEL CICLO DE VIDA DE LOS TRABAJOS
(RF-09, RF-10)
"""

import logging
import os
import signal
import threading
from datetime import datetime, timezone
from typing import Any

from .models import Job, JobStatus

logger = logging.getLogger("JobManager")

class JobManager:
    """
    PARA CONSULTAR, LISTAR Y CANCELAR
    TRABAJOS REGISTRADOS
    """
    def __init__(self, job_storage: dict[str, Job]) -> None:
        self.jobs = job_storage
        self._lock = threading.Lock()

    def list_jobs(self, status_filter: JobStatus | None = None) -> list[Job]:
        """
        MANDA LA LISTA DE TRABAJOS
        FILTRADO POR ESTADO
        """
        with self._lock:
            if status_filter is None:
                return list(self.jobs.values())
            return [job for job in self.jobs.values() if job.status == status_filter]

    def format_table(self, jobs: list[Job]) -> str:
        """
        VISTA PARA LA CLI CON METADATOS PRINCIPALES
        """
        if not jobs:
            return "No hay trabajos registrados"

        header = f"{'JOB ID':<38} {'PID':<8} {'ESTADO':<12} {'COMANDO'}"
        separator = "-" * 80
        lines = [header, separator]

        for job in jobs:
            pid_str = str(job.pid) if job.pid is not None else "-"
            cmd_str = " ".join(job.command)
            lines.append(f"{job.id:<38} {pid_str:<8} {job.status.value:<12} {cmd_str}")

        return "\n".join(lines)

    def cancel_job(self, job_id: str) -> tuple[bool, str]:
        """
        SOLICITAR CANCELACIÓN DE TRABAJO EN COLA
        O EJECUCIÓN Y RETORNAR LA TUPLA
        """
        with self._lock:
            job = self.jobs.get(job_id)
            if not job:
                return False, f"No se encontró ningún trabajo con ID {job_id}"

            # Caso 1: trabajo en cola
            if job.status == JobStatus.QUEUED:
                job.status = JobStatus.CANCELED
                job.finished_at = datetime.now(timezone.utc).isoformat()
                logger.info("Trabajo en cola %s cancelado exitosamente", job_id)
                return True, f"Trabajo {job_id} en cola cancelado exitosamente"

            # Caso 2: trabajo en ejecución
            if job.status == JobStatus.RUNNING:
                if job.pid is None:
                    job.status = JobStatus.FAILED
                    job.error_message = "Trabajo RUNNING sin PID registrado"
                    return False, "Error: el trabajo no tiene PID registrado"

                try:
                    # se llama a syscall kill(pid, SIGTERM)
                    os.kill(job.pid, signal.SIGTERM)
                    job.status = JobStatus.CANCELED
                    job.finished_at = datetime.now(timezone.utc).isoformat()
                    logger.info("Señal SIGTERM enviada al PID %d (Job %s)", job.pid, job_id)
                    return True, f"Señal de terminación enviada al PID {job.pid}. Estado: CANCELED"
                except ProcessLookupError:
                    # por si el proceso terminó antes de que llegue la señal
                    job.status = JobStatus.FAILED
                    job.finished_at = datetime.now(timezone.utc).isoformat()
                    return False, f"El proceso con PID {job.pid} ya había acabado"
                except PermissionError:
                    return False, f"Permiso denegado al intentar enviar señal al PID {job.pid}"

            # Caso 3: estados terminales
            return False, f"No se puede cancelar debido a que ya está en estado {job.status.value}"