import unittest
import threading

from src.executor import JobExecutor
from src.models import Job, JobStatus
from src.manager import JobManager


class JobManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.jobs: dict[str, Job] = {}
        self.manager = JobManager(self.jobs, JobExecutor(), threading.RLock())

    def test_lists_jobs_empty(self) -> None:
        self.assertEqual(self.manager.list_jobs(), [])
        self.assertIn("No hay trabajos", self.manager.format_table([]))

    def test_list_jobs_with_filter(self) -> None:
        job1 = Job(id="1", command = ["sleep", "10"], status = JobStatus.QUEUED)
        job2 = Job(id="2", command = ["ls"], status = JobStatus.RUNNING)
        self.jobs["1"] = job1
        self.jobs["2"] = job2

        all_jobs = self.manager.list_jobs()
        self.assertEqual(len(all_jobs), 2)

        queued_jobs = self.manager.list_jobs(status_filter = JobStatus.QUEUED)
        self.assertEqual(len(queued_jobs), 1)
        self.assertEqual(queued_jobs[0].id, "1")

    def test_cancel_queued_job(self) -> None:
        job = Job(id = "test-id", command = ["sleep", "5"], status = JobStatus.QUEUED)
        self.jobs["test-id"] = job

        success, msg = self.manager.cancel_job("test-id")
        self.assertTrue(success)
        self.assertEqual(job.status, JobStatus.CANCELED)
        self.assertIsNotNone(job.finished_at)

    def test_cancel_already_finished_job(self) -> None:
        job = Job(id = "test-id", command = ["echo", "1"], status = JobStatus.SUCCEEDED)
        self.jobs["test-id"] = job

        success, msg = self.manager.cancel_job("test-id")
        self.assertFalse(success)
        self.assertIn("SUCCEEDED", msg)

if __name__ == "__main__":
    unittest.main()