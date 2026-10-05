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


RawCommand: TypeAlias = str | list[str] | None  # Texto original o argumentos separados.

class JobSubmitter:
    """Valida solicitudes y registra trabajos sin encargarse de ejecutarlos.

    JobRunner proporciona el almacenamiento compartido; el resultado de este
    componente es un ID único y un Job inicialmente en estado QUEUED.
    """

    def __init__(self, job_storage: dict[str, Job] | None = None) -> None:
        # Si no se inyecta almacenamiento, sirve de forma independiente en pruebas.
        self.jobs = job_storage if job_storage is not None else {}
        # Evita colisiones al registrar solicitudes simultáneas.
        self._lock = threading.Lock()

    def validate_command(self, raw_command: RawCommand) -> list[str]:
        """Rechaza entradas inválidas y devuelve el comando separado en argumentos."""
        if raw_command is None:
            raise ValueError("RF-02: El comando no puede ser nulo (None).")

        if isinstance(raw_command, str):
            # `cleaned` quita espacios exteriores antes de verificar y separar.
            cleaned = raw_command.strip()
            if not cleaned:
                raise ValueError("RF-02: El comando no puede estar vacío.")
            try:
                # shlex respeta las comillas, pero no ejecuta el texto como shell.
                # `parsed_args` es la lista separada que recibirá subprocess.Popen.
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
            # En esta forma la persona que llama ya separó ejecutable y argumentos.
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
        """Registra una solicitud válida y devuelve su ID y objeto Job."""
        # Validar antes de generar el ID evita registros para solicitudes rechazadas.
        valid_args = self.validate_command(raw_command)
        # El ID se usa como llave en jobs y relaciona el Job con su proceso hijo.
        job_id = str(uuid.uuid4())
        # Job conserva los datos que luego comparten runner, executor y manager.
        new_job = Job(id=job_id, command=valid_args, status=JobStatus.QUEUED)
        with self._lock:
            # El lock protege el almacenamiento compartido ante envíos concurrentes.
            self.jobs[job_id] = new_job

        logger.info(
            "Trabajo aceptado con éxito | Job ID: %s | Comando: %r",
            job_id,
            valid_args,
        )

        return job_id, new_job