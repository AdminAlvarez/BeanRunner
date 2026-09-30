import logging
import shlex
import threading
import uuid
from typing import List, Dict, Union, Tuple, Optional
from models import Job, JobStatus

# Configuración de bitácora según RF-14
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [JobRunner] %(message)s"
)
logger = logging.getLogger("JobSubmitter")

class JobSubmitter:
    """
    Módulo encargado de la validación y recepción de trabajos,
    asignación de UUIDs únicos (RF-01, RF-02).
    """

    def __init__(self, job_storage: Optional[Dict[str, Job]] = None):
        # Almacenamiento central (o referencia a la cola compartida)
        self.jobs: Dict[str, Job] = job_storage if job_storage is not None else {}
        self._lock = threading.Lock()  # Garantiza Thread-Safety (RNF-27)

    def validate_command(self, raw_command: Union[str, List[str]]) -> List[str]:
        """
        RF-02: Valida la solicitud y rechaza entradas vacías o malformadas.
        """
        if raw_command is None:
            raise ValueError("RF-02: El comando no puede ser nulo (None).")

        # Si el usuario envía una cadena limpia (ej. "ls -la /tmp")
        if isinstance(raw_command, str):
            cleaned = raw_command.strip()
            if not cleaned:
                raise ValueError("RF-02: El comando no puede estar vacío.")
            try:
                # Divide respetando comillas 
                parsed_args = shlex.split(cleaned)
            except ValueError as e:
                raise ValueError(f"RF-02: Comando malformado o comillas sin cerrar: {e}")
        elif isinstance(raw_command, list):
            if not raw_command:
                raise ValueError("RF-02: La lista de comandos no puede estar vacía.")
            parsed_args = [str(arg).strip() for arg in raw_command if str(arg).strip()]
            if not parsed_args:
                raise ValueError("RF-02: Todos los argumentos de la lista estaban vacíos.")
        else:
            raise ValueError("RF-02: Formato no soportado. Debe ser string o list.")

        return parsed_args

    def submit_job(self, raw_command: Union[str, List[str]]) -> Tuple[str, Job]:
        """
        RF-01: Acepta un comando con sus argumentos y devuelve un ID único.
        """
        # 1. Validación de entradas (RF-02)
        valid_args = self.validate_command(raw_command)

        # 2. Generación de Identificador Único (UUID v4) (RF-01)
        job_id = str(uuid.uuid4())

        # 3. Instanciación del objeto Job
        new_job = Job(
            id=job_id,
            command=valid_args,
            status=JobStatus.QUEUED
        )

        # 4. Registro seguro en memoria compartida (RNF-27)
        with self._lock:
            self.jobs[job_id] = new_job

        # 5. Bitácora de auditoría (RF-14)
        logger.info(f"Trabajo aceptado con éxito | Job ID: {job_id} | Comando: '{' '.join(valid_args)}'")

        return job_id, new_job