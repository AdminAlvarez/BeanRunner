import subprocess
import sys
import unittest
from pathlib import Path


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
            "[BeanRunner] Servicio JobRunner inicializado correctamente.\n",
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


if __name__ == "__main__":
    unittest.main()
