import argparse

from .job_runner import JobRunner


def main():
    parser = argparse.ArgumentParser(
        description="BeanRunner - Job Runner"
    )

    parser.add_argument(
        "--demo",
        action="store_true",
        help="Ejecuta una demostración del sistema"
    )

    args = parser.parse_args()

    runner = JobRunner()

    if args.demo:
        print("=== BeanRunner ===")
        print("JobRunner iniciado")

        job = runner.submit_job([
            "python3",
            "src/test-jobs/simple_job.py"
        ])

        print(f"Job creado: {job.id}")
        print(f"Estado: {job.status.value}")

    else:
        print("BeanRunner iniciado")
        print("Use --demo para ejecutar una demostración")


if __name__ == "__main__":
    main()