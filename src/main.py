"""Command-line entry point and local interactive shell for BeanRunner."""

import argparse
import json
import shlex
import sys
import time
from collections.abc import Sequence
from typing import TextIO

from .Job_Runner import JobRunner
from .models import Job, JobStatus
from .submitter import JobSubmitter


DEMO_COMMANDS: tuple[str | list[str], ...] = (
    "sleep 10",
    "python3 -c \"print('Hola Mundo')\"",
    ["ls", "-l", "/var/log"],
    "",
    "   ",
    'echo "comillas sin cerrar',
)
TERMINAL_STATUSES = {
    JobStatus.SUCCEEDED,
    JobStatus.FAILED,
    JobStatus.CANCELED,
}
HELP_TEXT = """Comandos disponibles:
  submit <comando>       Envia un trabajo local (no se usa un shell).
  status <job-id>        Consulta el estado y metadatos.
  list [estado]          Lista trabajos; estado puede ser QUEUED, RUNNING,
                         SUCCEEDED, FAILED o CANCELED.
  output <job-id>        Muestra stdout y stderr cuando estén disponibles.
  cancel <job-id>        Solicita cancelar un trabajo.
  help                   Muestra esta ayuda.
  exit                   Sale y cancela los trabajos todavía activos.

Ejemplo: submit python -c "print('hola')"
"""


def run_submission_demo() -> None:
    """Demonstrate valid and invalid submissions without running commands."""
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
    """Run a long sample, show it running, cancel it, and report its result."""
    runner = JobRunner()
    job = runner.submit_job([sys.executable, "src/job_tests/long_job.py"])

    print(f"Trabajo creado: {job.id}")
    print(f"Estado inicial: {job.status.value}")
    print(f"PID: {job.pid}")
    time.sleep(1)
    print("\n--- Trabajos activos ---")
    print(runner.manager.format_table(runner.list_jobs()))

    success, message = runner.cancel_job(job.id)
    print(f"\n[{'PASS' if success else 'FAIL'}] {message}")
    wait_for_job(runner, job.id)
    print_job_result(job)


def wait_for_job(runner: JobRunner, job_id: str, timeout: float = 5.0) -> bool:
    """Wait briefly for a background process to reach a terminal status."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if runner.get_status(job_id) in TERMINAL_STATUSES:
            return True
        time.sleep(0.01)
    return runner.get_status(job_id) in TERMINAL_STATUSES


def print_job_result(job: Job, output: TextIO = sys.stdout) -> None:
    """Print the final status and captured streams for a job."""
    print("\n--- RESULTADO ---", file=output)
    print(f"Estado final: {job.status.value}", file=output)
    print(f"Código de salida: {job.exit_code}", file=output)
    print(f"STDOUT:\n{job.stdout}", file=output)
    print(f"STDERR:\n{job.stderr}", file=output)


def interactive_loop(
    input_stream: TextIO = sys.stdin,
    output_stream: TextIO = sys.stdout,
    runner: JobRunner | None = None,
) -> int:
    """Read local commands until exit or end-of-file."""
    job_runner = runner if runner is not None else JobRunner()
    print("BeanRunner local. Escribe 'help' para ver comandos.", file=output_stream)

    while True:
        print("beanrunner> ", end="", file=output_stream, flush=True)
        line = input_stream.readline()
        if not line:
            break

        try:
            tokens = shlex.split(line)
        except ValueError as error:
            print(f"Error: comando mal formado: {error}", file=output_stream)
            continue
        if not tokens:
            continue

        action = tokens[0].lower()
        if action in {"exit", "quit"}:
            break
        if action == "help":
            print(HELP_TEXT, file=output_stream, end="")
            continue
        if action == "submit":
            _, separator, command = line.strip().partition(" ")
            if not separator or not command.strip():
                print("Uso: submit <comando>", file=output_stream)
                continue
            try:
                job = job_runner.submit_job(command.strip())
            except ValueError as error:
                print(f"Solicitud rechazada: {error}", file=output_stream)
                continue
            print(
                f"Trabajo aceptado: {job.id} (estado: {job.status.value})",
                file=output_stream,
            )
            continue
        if action == "status":
            if len(tokens) != 2:
                print("Uso: status <job-id>", file=output_stream)
                continue
            job = job_runner.get_job(tokens[1])
            if job is None:
                print(f"No se encontró el trabajo {tokens[1]}.", file=output_stream)
            else:
                print(
                    json.dumps(job.to_dict(), ensure_ascii=False, indent=2),
                    file=output_stream,
                )
            continue
        if action == "list":
            if len(tokens) > 2:
                print("Uso: list [estado]", file=output_stream)
                continue
            try:
                status_filter = (
                    JobStatus[tokens[1].upper()] if len(tokens) == 2 else None
                )
            except KeyError:
                valid_statuses = ", ".join(status.name for status in JobStatus)
                print(
                    f"Estado inválido. Usa uno de: {valid_statuses}",
                    file=output_stream,
                )
                continue
            print(
                job_runner.manager.format_table(
                    job_runner.list_jobs(status_filter)
                ),
                file=output_stream,
            )
            continue
        if action == "cancel":
            if len(tokens) != 2:
                print("Uso: cancel <job-id>", file=output_stream)
                continue
            success, message = job_runner.cancel_job(tokens[1])
            label = "PASS" if success else "ERROR"
            print(f"[{label}] {message}", file=output_stream)
            continue
        if action == "output":
            if len(tokens) != 2:
                print("Uso: output <job-id>", file=output_stream)
                continue
            job = job_runner.get_job(tokens[1])
            if job is None:
                print(f"No se encontró el trabajo {tokens[1]}.", file=output_stream)
                continue
            if job.status not in TERMINAL_STATUSES:
                print("El trabajo sigue activo; intenta de nuevo más tarde.", file=output_stream)
                continue
            print(f"STDOUT:\n{job.stdout}", file=output_stream)
            print(f"STDERR:\n{job.stderr}", file=output_stream)
            continue

        print(f"Comando desconocido: {action}. Escribe 'help'.", file=output_stream)

    job_runner.shutdown()
    print("BeanRunner detenido.", file=output_stream)
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Parse options and launch the requested local mode."""
    parser = argparse.ArgumentParser(description="BeanRunner JobRunner local")
    demonstrations = parser.add_mutually_exclusive_group()
    demonstrations.add_argument(
        "--demo",
        action="store_true",
        help="demuestra validación y recepción (RF-01/RF-02)",
    )
    demonstrations.add_argument(
        "--run-job-demo",
        action="store_true",
        help="ejecuta y cancela un trabajo local de ejemplo",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="inicia la CLI local para enviar y controlar trabajos",
    )
    arguments = parser.parse_args(argv)

    if arguments.interactive:
        return interactive_loop()
    if arguments.run_job_demo:
        run_job_demo()
    elif arguments.demo:
        run_submission_demo()
    else:
        print("[BeanRunner] Servicio JobRunner inicializado correctamente.")
        print("Para trabajar localmente, ejecuta: python -m src.main --interactive")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
