import sys
import time
import unittest

from src.Job_Runner import JobRunner
from src.models import JobStatus


class JobRunnerTests(unittest.TestCase):
    def wait_for_completion(self, runner: JobRunner, job_id: str) -> JobStatus:
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            status = runner.get_status(job_id)
            if status in (JobStatus.SUCCEEDED, JobStatus.FAILED, JobStatus.CANCELED):
                return status
            time.sleep(0.01)
        self.fail(f"Job {job_id} did not finish within the timeout")

    def test_submission_uses_validated_shared_job_storage(self) -> None:
        runner = JobRunner()

        with self.assertRaisesRegex(ValueError, "RF-02"):
            runner.submit_job('echo "unfinished')

        job = runner.submit_job([sys.executable, "-c", "print('runner ok')"])
        self.assertEqual(runner.jobs, {job.id: job})
        self.assertEqual(runner.queue, [job.id])

    def test_successful_process_records_output_and_exit_code(self) -> None:
        runner = JobRunner()
        job = runner.submit_job([sys.executable, "-c", "print('runner ok')"])

        runner.execute_job(job.id)

        self.assertEqual(self.wait_for_completion(runner, job.id), JobStatus.SUCCEEDED)
        self.assertEqual(job.exit_code, 0)
        self.assertEqual(job.stdout, "runner ok\n")
        self.assertEqual(job.stderr, "")
        self.assertIsNotNone(job.started_at)
        self.assertIsNotNone(job.finished_at)

    def test_failed_process_records_nonzero_exit_code(self) -> None:
        runner = JobRunner()
        job = runner.submit_job([sys.executable, "-c", "raise SystemExit(7)"])

        runner.execute_job(job.id)

        self.assertEqual(self.wait_for_completion(runner, job.id), JobStatus.FAILED)
        self.assertEqual(job.exit_code, 7)

    def test_launch_failure_marks_job_failed_without_raising(self) -> None:
        runner = JobRunner()
        job = runner.submit_job(["__beanrunner_missing_executable__"])

        runner.execute_job(job.id)

        self.assertEqual(job.status, JobStatus.FAILED)
        self.assertIsNotNone(job.error_message)
        self.assertIsNotNone(job.finished_at)


if __name__ == "__main__":
    unittest.main()
