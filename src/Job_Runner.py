# job_runner.py

from .job import Job


class JobRunner:

    def __init__(self):
        self.jobs = {}
        self.queue = []

    def submit_job(self, command):
        job = Job(command)

        self.jobs[job.id] = job
        self.queue.append(job.id)

        return job