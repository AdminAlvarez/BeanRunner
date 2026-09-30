import logging
import shlex
import threading
import uuid
from typing import TypeAlias

from .models import Job, JobStatus


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [JobRunner] %(message)s",
)
logger = logging.getLogger("JobSubmitter")


RawCommand: TypeAlias = str | list[str] | None


class JobSubmitter:
    """Validate job submissions and assign unique identifiers."""

    def __init__(self, job_storage: dict[str, Job] | None = None) -> None:
        self.jobs = job_storage if job_storage is not None else {}
        self._lock = threading.Lock()

    def validate_command(self, raw_command: RawCommand) -> list[str]:
        """Reject empty or malformed commands and return parsed arguments."""
        if raw_command is None:
            raise ValueError("RF-02: El comando no puede ser nulo (None).")

        if isinstance(raw_command, str):
            cleaned = raw_command.strip()
            if not cleaned:
                raise ValueError("RF-02: El comando no puede estar vacío.")
            try:
                parsed_args = shlex.split(cleaned, posix=True)
            except ValueError as error:
                raise ValueError(
                    f"RF-02: Comando malformado o comillas sin cerrar: {error}"
                ) from error
        elif isinstance(raw_command, list):
            if not raw_command:
                raise ValueError("RF-02: La lista de comandos no puede estar vacía.")
            if any(not isinstance(argument, str) for argument in raw_command):
                raise ValueError("RF-02: Todos los argumentos deben ser texto.")
            parsed_args = [argument.strip() for argument in raw_command if argument.strip()]
            if not parsed_args:
                raise ValueError(
                    "RF-02: Todos los argumentos de la lista estaban vacíos."
                )
        else:
            raise ValueError(
                "RF-02: Formato no soportado. Debe ser string o list."
            )

        if not parsed_args:
            raise ValueError("RF-02: El comando no puede estar vacío.")

        return parsed_args

    def submit_job(self, raw_command: RawCommand) -> tuple[str, Job]:
        """Accept a valid command and return its unique ID and queued job."""
        valid_args = self.validate_command(raw_command)
        job_id = str(uuid.uuid4())
        new_job = Job(id=job_id, command=valid_args, status=JobStatus.QUEUED)
        with self._lock:
            self.jobs[job_id] = new_job

        logger.info(
            "Trabajo aceptado con éxito | Job ID: %s | Comando: %r",
            job_id,
            valid_args,
        )

        return job_id, new_job