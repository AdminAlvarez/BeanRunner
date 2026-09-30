"""BeanRunner application entry point."""

import argparse
from collections.abc import Sequence

from .submitter import JobSubmitter


DEMO_COMMANDS: tuple[str | list[str], ...] = (
    "sleep 10",
    "python3 -c \"print('Hola Mundo')\"",
    ["ls", "-l", "/var/log"],
    "",
    "   ",
    'echo "comillas sin cerrar',
)


def run_demo() -> None:
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


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="BeanRunner JobRunner")
    parser.add_argument(
        "--demo",
        action="store_true",
        help="demuestra la validación y recepción de trabajos (RF-01/RF-02)",
    )
    arguments = parser.parse_args(argv)

    if arguments.demo:
        run_demo()
    else:
        print("[BeanRunner] Servicio JobRunner inicializado correctamente.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
