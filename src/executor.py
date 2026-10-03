import subprocess
import threading
from datetime import datetime, timezone

from .models import Job, JobStatus


class JobExecutor:

    def __init__(self):
        self.processes = {}

    def execute(self, job: Job):
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
            return

        job.pid = process.pid
        job.started_at = datetime.now(timezone.utc).isoformat()
        job.status = JobStatus.RUNNING

        self.processes[job.id] = process

        monitor = threading.Thread(
            target=self._monitor_process,
            args=(job, process),
            daemon=True
        )

        monitor.start()

    def _monitor_process(self, job: Job, process):

        stdout, stderr = process.communicate()

        job.stdout = stdout
        job.stderr = stderr
        job.exit_code = process.returncode
        job.finished_at = datetime.now(timezone.utc).isoformat()

        if job.status != JobStatus.CANCELED:
            if process.returncode == 0:
                job.status = JobStatus.SUCCEEDED
            else:
                job.status = JobStatus.FAILED

        self.processes.pop(job.id, None)

    def get_process(self, job_id):
        return self.processes.get(job_id)