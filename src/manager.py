"""Query and cancel jobs stored by a JobRunner instance."""

import logging
import threading
from datetime import datetime, timezone

from .executor import JobExecutor
from .models import Job, JobStatus


logger = logging.getLogger("JobManager")


class JobManager:
    """Provide operations for looking up, listing, and canceling jobs."""

    def __init__(
        self,
        job_storage: dict[str, Job],
        executor: JobExecutor,
        lock: threading.RLock,
    ) -> None:
        self.jobs = job_storage
        self.executor = executor
        self._lock = lock

    def get_job(self, job_id: str) -> Job | None:
        """Return the job with this ID, or None when it is unknown."""
        with self._lock:
            return self.jobs.get(job_id)

    def list_jobs(self, status_filter: JobStatus | None = None) -> list[Job]:
        """Return all jobs, optionally filtering by lifecycle status."""
        with self._lock:
            jobs = list(self.jobs.values())
            if status_filter is None:
                return jobs
            return [job for job in jobs if job.status == status_filter]

    def format_table(self, jobs: list[Job]) -> str:
        """Format job metadata as a readable table for terminal use."""
        if not jobs:
            return "No hay trabajos registrados."

        header = f"{'JOB ID':<36} {'PID':<8} {'ESTADO':<12} {'CÓDIGO':<8} COMANDO"
        separator = "-" * len(header)
        lines = [header, separator]

        for job in jobs:
            pid = str(job.pid) if job.pid is not None else "-"
            exit_code = str(job.exit_code) if job.exit_code is not None else "-"
            command = " ".join(job.command)
            lines.append(
                f"{job.id:<36} {pid:<8} {job.status.value:<12} "
                f"{exit_code:<8} {command}"
            )

        return "\n".join(lines)

    def cancel_job(self, job_id: str) -> tuple[bool, str]:
        """Cancel a queued job or request termination of its running process."""
        with self._lock:
            job = self.jobs.get(job_id)
            if job is None:
                return False, f"No se encontró ningún trabajo con ID {job_id}."

            if job.status == JobStatus.QUEUED:
                job.status = JobStatus.CANCELED
                job.finished_at = datetime.now(timezone.utc).isoformat()
                logger.info("Trabajo en cola %s cancelado.", job_id)
                return True, f"Trabajo {job_id} cancelado antes de ejecutarse."

            if job.status != JobStatus.RUNNING:
                return (
                    False,
                    f"No se puede cancelar: el trabajo está en estado {job.status.value}.",
                )

            success, message = self.executor.cancel(job)
            if success:
                logger.info("Se solicitó cancelar el trabajo %s.", job_id)
            return success, message
