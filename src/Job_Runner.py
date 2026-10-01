from .job import Job, JobStatus
from .executor import JobExecutor


class JobRunner:

    def __init__(self):
        self.jobs = {}
        self.queue = []

        self.executor = JobExecutor()

    def submit_job(self, command):

        job = Job(command)

        self.jobs[job.id] = job
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