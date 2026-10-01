import subprocess
import threading
from datetime import datetime

from .job import Job, JobStatus


class JobExecutor:

    def __init__(self):
        self.processes = {}

    def execute(self, job: Job):

        process = subprocess.Popen(
            job.command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        job.pid = process.pid
        job.started_at = datetime.now()
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
        job.finished_at = datetime.now()

        if process.returncode == 0:
            job.status = JobStatus.SUCCEEDED
        else:
            job.status = JobStatus.FAILED

        del self.processes[job.id]

    def get_process(self, job_id):
        return self.processes.get(job_id)