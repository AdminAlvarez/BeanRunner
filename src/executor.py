import subprocess
from datetime import datetime

from job import Job, JobStatus


class JobExecutor:

    def execute(self, job: Job):

        job.status = JobStatus.RUNNING
        job.started_at = datetime.now()

        process = subprocess.Popen(
            job.command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        job.pid = process.pid

        stdout, stderr = process.communicate()

        job.stdout = stdout
        job.stderr = stderr
        job.exit_code = process.returncode
        job.finished_at = datetime.now()

        if process.returncode == 0:
            job.status = JobStatus.SUCCEEDED
        else:
            job.status = JobStatus.FAILED

        return job