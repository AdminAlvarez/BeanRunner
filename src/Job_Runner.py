from .models import Job, JobStatus
from .executor import JobExecutor
from .submitter import JobSubmitter
from .manager import JobManager

class JobRunner:
    def __init__(self):
        self.jobs: dict[str, Job] = {}
        self.queue = []

        self.submitter = JobSubmitter(self.jobs)
        self.executor = JobExecutor()
        self.manager = JobManager(self.jobs)

    def submit_job(self, command):
        _, job = self.submitter.submit_job(command)
        self.queue.append(job.id)
        return job

    def execute_job(self, job_id):
        job = self.jobs.get(job_id)
        if job is None:
            return None
        if job.status != JobStatus.QUEUED:
            return job

        self.queue.remove(job_id)
        self.executor.execute(job)
        return job

    def get_job(self, job_id):
        return self.jobs.get(job_id)

    def get_status(self, job_id):
        job = self.jobs.get(job_id)
        if job is None:
            return None
        return job.status
