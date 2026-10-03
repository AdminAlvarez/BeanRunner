"""Coordinate local job submission, execution, and lifecycle queries."""

import threading
from collections import deque
from datetime import datetime, timezone

from .executor import JobExecutor
from .manager import JobManager
from .models import Job, JobStatus
from .submitter import JobSubmitter, RawCommand


class JobRunner:
    """Keep jobs in memory and run up to max_concurrency child processes."""

    def __init__(self, max_concurrency: int = 3) -> None:
        if max_concurrency < 1:
            raise ValueError("max_concurrency debe ser al menos 1.")

        self.jobs: dict[str, Job] = {}
        self.queue: deque[str] = deque()
        self.max_concurrency = max_concurrency
        self._lock = threading.RLock()
        self._shutting_down = False
        self.submitter = JobSubmitter(self.jobs)
        self.executor = JobExecutor()
        self.manager = JobManager(self.jobs, self.executor, self._lock)

    def submit_job(self, command: RawCommand) -> Job:
        """Validate, register, queue, and start a job when capacity is free."""
        with self._lock:
            _, job = self.submitter.submit_job(command)
            self.queue.append(job.id)
            self._start_queued_jobs()
            return job

    def execute_job(self, job_id: str) -> Job | None:
        """Start queued work if possible; retained for existing callers."""
        with self._lock:
            job = self.jobs.get(job_id)
            if job is None:
                return None
            self._start_queued_jobs()
            return job

    def get_job(self, job_id: str) -> Job | None:
        """Return all metadata for a job, or None when the ID is unknown."""
        return self.manager.get_job(job_id)

    def get_status(self, job_id: str) -> JobStatus | None:
        """Return a job's current status, or None when it is unknown."""
        job = self.get_job(job_id)
        return job.status if job is not None else None

    def list_jobs(self, status_filter: JobStatus | None = None) -> list[Job]:
        """List registered jobs, optionally filtering by status."""
        return self.manager.list_jobs(status_filter)

    def cancel_job(self, job_id: str) -> tuple[bool, str]:
        """Cancel a queued job or stop a running child process."""
        with self._lock:
            result = self.manager.cancel_job(job_id)
            self._start_queued_jobs()
            return result

    def shutdown(self) -> None:
        """Stop accepting queued work and terminate active child processes."""
        with self._lock:
            self._shutting_down = True
            for job_id in tuple(self.queue):
                job = self.jobs.get(job_id)
                if job is not None and job.status == JobStatus.QUEUED:
                    job.status = JobStatus.CANCELED
                    job.finished_at = datetime.now(timezone.utc).isoformat()
            self.queue.clear()

            running_jobs = [
                job for job in self.jobs.values() if job.status == JobStatus.RUNNING
            ]

        for job in running_jobs:
            self.manager.cancel_job(job.id)

    def _start_queued_jobs(self) -> None:
        """Fill free process slots while preserving FIFO queue order."""
        if self._shutting_down:
            return
        while self.queue and self.executor.active_count < self.max_concurrency:
            job_id = self.queue.popleft()
            job = self.jobs.get(job_id)
            if job is None or job.status != JobStatus.QUEUED:
                continue
            self.executor.execute(job, self._on_job_finished)

    def _on_job_finished(self, _job: Job) -> None:
        """Start the next queued job as soon as a process slot is released."""
        with self._lock:
            self._start_queued_jobs()
