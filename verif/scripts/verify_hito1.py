#!/usr/bin/env python3
"""Run end-to-end local checks for the BeanRunner milestone."""

import subprocess
import sys
import time
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.Job_Runner import JobRunner
from src.models import JobStatus


TERMINAL_STATUSES = {
    JobStatus.SUCCEEDED,
    JobStatus.FAILED,
    JobStatus.CANCELED,
}


def wait_for_terminal_status(
    runner: JobRunner,
    job_id: str,
    timeout_seconds: float = 5.0,
) -> JobStatus:
    """Wait for an asynchronous child process and fail on timeout."""
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        status = runner.get_status(job_id)
        if status in TERMINAL_STATUSES:
            return status
        time.sleep(0.01)
    raise AssertionError(f"El trabajo {job_id} no terminó a tiempo.")


def verify_application_startup() -> None:
    """Check the documented program entry point and successful exit."""
    result = subprocess.run(
        [sys.executable, "-m", "src.main"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        check=False,
        text=True,
    )
    expected = (
        "[BeanRunner] Servicio JobRunner inicializado correctamente.\n"
        "Para trabajar localmente, ejecuta: python -m src.main --interactive\n"
    )
    if result.returncode != 0 or result.stdout != expected or result.stderr:
        raise AssertionError(
            "El punto de entrada no produjo el inicio esperado. "
            f"exit={result.returncode}, stdout={result.stdout!r}, "
            f"stderr={result.stderr!r}"
        )


def verify_invalid_then_valid_request() -> None:
    """Check that rejected input does not poison later valid submissions."""
    runner = JobRunner()
    try:
        runner.submit_job('echo "comillas sin cerrar')
    except ValueError as error:
        if "RF-02" not in str(error):
            raise AssertionError(f"Mensaje de validación inesperado: {error}") from error
    else:
        raise AssertionError("Se aceptó un comando con comillas sin cerrar.")

    if runner.jobs:
        raise AssertionError("La solicitud inválida dejó un trabajo registrado.")

    job = runner.submit_job([sys.executable, "-c", "print('BeanRunner OK')"])
    status = wait_for_terminal_status(runner, job.id)
    if status != JobStatus.SUCCEEDED or job.exit_code != 0:
        raise AssertionError(
            f"La solicitud válida posterior falló: status={status}, "
            f"exit_code={job.exit_code}"
        )
    if job.stdout != "BeanRunner OK\n" or job.stderr:
        raise AssertionError(
            f"Captura inesperada: stdout={job.stdout!r}, stderr={job.stderr!r}"
        )


def verify_nonzero_exit_code() -> None:
    """Check that an unsuccessful child is marked failed with its exit code."""
    runner = JobRunner()
    job = runner.submit_job([sys.executable, "-c", "raise SystemExit(7)"])
    status = wait_for_terminal_status(runner, job.id)
    if status != JobStatus.FAILED or job.exit_code != 7:
        raise AssertionError(
            f"Resultado incorrecto: status={status}, exit_code={job.exit_code}"
        )


def verify_running_job_cancellation() -> None:
    """Check that cancel terminates a real active child and records the result."""
    runner = JobRunner()
    job = runner.submit_job(
        [sys.executable, "-c", "import time; time.sleep(30)"]
    )
    if job.status != JobStatus.RUNNING:
        raise AssertionError(f"El trabajo no inició: status={job.status}")

    canceled, message = runner.cancel_job(job.id)
    if not canceled:
        raise AssertionError(f"No se pudo cancelar el trabajo: {message}")
    status = wait_for_terminal_status(runner, job.id)
    if status != JobStatus.CANCELED:
        raise AssertionError(f"La cancelación terminó en estado {status}.")
    if runner.executor.get_process(job.id) is not None:
        raise AssertionError("El proceso cancelado continúa registrado como activo.")


def main() -> int:
    checks = (
        ("inicio de aplicación", verify_application_startup),
        ("entrada inválida y recuperación", verify_invalid_then_valid_request),
        ("código de salida no cero", verify_nonzero_exit_code),
        ("cancelación de proceso activo", verify_running_job_cancellation),
    )

    failures = 0
    for description, check in checks:
        try:
            check()
        except (AssertionError, OSError, ValueError) as error:
            failures += 1
            print(f"[FAIL] {description}: {error}")
        else:
            print(f"[PASS] {description}")

    print(f"Resultado: {len(checks) - failures}/{len(checks)} verificaciones aprobadas.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
