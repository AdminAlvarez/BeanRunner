import subprocess
import sys
import unittest
from io import StringIO
from pathlib import Path

from src.Job_Runner import JobRunner
from src.main import interactive_loop, wait_for_job
from src.models import JobStatus


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class MainTests(unittest.TestCase):
    def test_entry_point_reports_successful_startup(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "src.main"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            check=False,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout,
            "[BeanRunner] Servicio JobRunner inicializado correctamente.\n"
            "Para trabajar localmente, ejecuta: python -m src.main --interactive\n",
        )
        self.assertEqual(result.stderr, "")

    def test_demo_preserves_job_submission_examples(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "src.main", "--demo"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            check=False,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("[PASS] Asignado ID único:", result.stdout)
        self.assertIn("[RECHAZADO] Error detectado (RF-02):", result.stdout)

    def test_interactive_mode_recovers_from_invalid_command_and_accepts_job(self) -> None:
        runner = JobRunner()
        commands = StringIO(
            'submit echo "comillas incompletas\n'
            "submit python -c \"print('cli funciona')\"\n"
            "list\n"
            "exit\n"
        )
        output = StringIO()

        result = interactive_loop(commands, output, runner)

        self.assertEqual(result, 0)
        self.assertIn("comando mal formado", output.getvalue())
        self.assertIn("Trabajo aceptado:", output.getvalue())
        self.assertIn("JOB ID", output.getvalue())
        self.assertEqual(len(runner.jobs), 1)
        job = next(iter(runner.jobs.values()))
        self.assertTrue(wait_for_job(runner, job.id))
        self.assertIn(
            job.status,
            (JobStatus.SUCCEEDED, JobStatus.CANCELED),
        )

    def test_interactive_mode_queries_job_and_reports_unknown_ids(self) -> None:
        runner = JobRunner()
        job = runner.submit_job([sys.executable, "-c", "print('query output')"])
        self.assertTrue(wait_for_job(runner, job.id))

        output = StringIO()
        commands = StringIO(
            f"status {job.id}\n"
            "status missing-id\n"
            f"output {job.id}\n"
            "output missing-id\n"
            "list INVALID\n"
            "exit\n"
        )
        interactive_loop(commands, output, runner)

        text = output.getvalue()
        self.assertIn('"status": "SUCCEEDED"', text)
        self.assertIn("query output", text)
        self.assertIn("No se encontró el trabajo missing-id", text)
        self.assertIn("Estado inválido", text)


if __name__ == "__main__":
    unittest.main()
