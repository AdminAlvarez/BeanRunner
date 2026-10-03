"""Launch and monitor job processes."""

import logging
import subprocess
import threading
from collections.abc import Callable
from datetime import datetime, timezone

from .models import Job, JobStatus


logger = logging.getLogger("JobExecutor")
CompletionCallback = Callable[[Job], None]


class JobExecutor:
    """Run each job in a child process and collect its result asynchronously."""

    def __init__(self) -> None:
        self.processes: dict[str, subprocess.Popen[str]] = {}
        self._lock = threading.Lock()

    def execute(
        self,
        job: Job,
        on_complete: CompletionCallback | None = None,
    ) -> bool:
        """Start a job and return whether its child process was launched."""
        try:
            process = subprocess.Popen(
                job.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        except OSError as error:
            job.status = JobStatus.FAILED
            job.error_message = str(error)
            job.finished_at = datetime.now(timezone.utc).isoformat()
            logger.error("No se pudo iniciar el trabajo %s: %s", job.id, error)
            return False

        job.pid = process.pid
        job.started_at = datetime.now(timezone.utc).isoformat()
        job.status = JobStatus.RUNNING

        with self._lock:
            self.processes[job.id] = process

        monitor = threading.Thread(
            target=self._monitor_process,
            args=(job, process, on_complete),
            name=f"beanrunner-job-{job.id}",
            daemon=True,
        )
        monitor.start()
        return True

    def cancel(self, job: Job, grace_seconds: float = 1.0) -> tuple[bool, str]:
        """Terminate a running child, escalating to kill after a short grace."""
        with self._lock:
            process = self.processes.get(job.id)
            if process is None or process.poll() is not None:
                return False, "El proceso ya terminó o no está activo."

            job.cancel_requested = True
            try:
                process.terminate()
            except OSError as error:
                job.cancel_requested = False
                logger.error("No se pudo terminar el trabajo %s: %s", job.id, error)
                return False, f"No se pudo terminar el proceso: {error}"

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
        """Return the active process for a job, if it is still being monitored."""
        with self._lock:
            return self.processes.get(job_id)

    @property
    def active_count(self) -> int:
        """Return the number of child processes that are still being monitored."""
        with self._lock:
            return len(self.processes)

    def _monitor_process(
        self,
        job: Job,
        process: subprocess.Popen[str],
        on_complete: CompletionCallback | None,
    ) -> None:
        try:
            stdout, stderr = process.communicate()
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
            with self._lock:
                self.processes.pop(job.id, None)
            if on_complete is not None:
                on_complete(job)
