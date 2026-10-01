import sys
import time

from .job_runner import JobRunner


def main():

    runner = JobRunner()

    job = runner.submit_job([
        sys.executable,
        "src/job_tests/long_job.py"
    ])

    print(f"Job creado: {job.id}")
    print(f"Estado inicial: {job.status.value}")

    runner.execute_job(job.id)

    print(f"PID: {job.pid}")
    print(f"Estado después de ejecutar: {job.status.value}")

    while True:

        time.sleep(1)

        status = runner.get_status(job.id)

        print(f"Estado actual: {status.value}")

        if status.value in ["SUCCEEDED", "FAILED", "CANCELED"]:
            break

    print("\n--- RESULTADO ---")
    print(f"Estado final: {job.status.value}")
    print(f"Código de salida: {job.exit_code}")
    print(f"STDOUT:\n{job.stdout}")
    print(f"STDERR:\n{job.stderr}")


if __name__ == "__main__":
    main()