"""BeanRunner application entry point."""

import argparse
import sys
import time
from collections.abc import Sequence

from .Job_Runner import JobRunner
from .models import JobStatus
from .submitter import JobSubmitter


DEMO_COMMANDS: tuple[str | list[str], ...] = (
    "sleep 10",
    "python3 -c \"print('Hola Mundo')\"",
    ["ls", "-l", "/var/log"],
    "",
    "   ",
    'echo "comillas sin cerrar',
)


def run_submission_demo() -> None:
    """Exercise the RF-01/RF-02 submission examples without running commands."""
    submitter = JobSubmitter()
    print("=== Módulo de Envío de Trabajos (JobRunner - RF-01 & RF-02) ===")

    for command in DEMO_COMMANDS:
        print(f"\nProcesando entrada: {command!r}")
        try:
            job_id, job = submitter.submit_job(command)
        except ValueError as error:
            print(f"  [RECHAZADO] Error detectado (RF-02): {error}")
        else:
            print(f"  [PASS] Asignado ID único: {job_id}")
            print(f"  [INFO] Estado inicial: {job.status.value}")


def run_job_demo() -> None:
    """Run a local sample process and report its final status and output."""
    runner = JobRunner()
    job = runner.submit_job([
        sys.executable,
        "src/job_tests/long_job.py",
    ])

    print(f"Job creado: {job.id}")
    print(f"Estado inicial: {job.status.value}")
    runner.execute_job(job.id)
    print(f"PID: {job.pid}")
    print(f"Estado después de ejecutar: {job.status.value}")

    while True:
        time.sleep(0.1)
        status = runner.get_status(job.id)
        if status is None:
            raise RuntimeError(f"No se encontró el trabajo {job.id}")
        print(f"Estado actual: {status.value}")
        if status in (JobStatus.SUCCEEDED, JobStatus.FAILED, JobStatus.CANCELED):
            break

    print("\n--- RESULTADO ---")
    print(f"Estado final: {job.status.value}")
    print(f"Código de salida: {job.exit_code}")
    print(f"STDOUT:\n{job.stdout}")
    print(f"STDERR:\n{job.stderr}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="BeanRunner JobRunner")
    demonstrations = parser.add_mutually_exclusive_group()
    demonstrations.add_argument(
        "--demo",
        action="store_true",
        help="demuestra la validación y recepción de trabajos (RF-01/RF-02)",
    )
    demonstrations.add_argument(
        "--run-job-demo",
        action="store_true",
        help="ejecuta un trabajo local de ejemplo y consulta su estado",
    )
    arguments = parser.parse_args(argv)

    if arguments.run_job_demo:
        run_job_demo()
    elif arguments.demo:
        run_submission_demo()
    else:
        print("[BeanRunner] Servicio JobRunner inicializado correctamente.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
