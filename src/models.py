from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class JobStatus(str, Enum):
    """Estados que puede tener un trabajo durante su ciclo de vida."""

    # Aceptado, pero aún no tiene un proceso hijo asignado.
    QUEUED = "QUEUED"
    # El proceso hijo está activo y siendo supervisado.
    RUNNING = "RUNNING"
    # Estado terminal: proceso terminó con código de salida 0.
    SUCCEEDED = "SUCCEEDED"
    # Estado terminal: hubo error al iniciar o el proceso terminó distinto de 0.
    FAILED = "FAILED"
    # Estado terminal: usuario o cierre de CLI solicitó detenerlo.
    CANCELED = "CANCELED"


@dataclass
class Job:
    """Datos compartidos del trabajo entre runner, executor, manager y CLI."""

    # Argumentos del programa: el primer elemento es el ejecutable.
    command: list[str]
    # UUID usado para buscar el trabajo en los componentes de BeanRunner.
    id: str = field(default_factory=lambda: str(uuid4()))
    # Estado consultado por runner, manager y CLI; inicia antes de ejecutar.
    status: JobStatus = JobStatus.QUEUED
    # Fechas UTC en formato ISO; inicio y fin son None hasta que ocurren.
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    # Momento en que executor inició el proceso hijo.
    started_at: str | None = None
    # Momento en que executor recogió el resultado final.
    finished_at: str | None = None
    # Resultado del proceso hijo; None significa que aún no hay código final.
    exit_code: int | None = None
    # PID del sistema operativo, disponible solo después de iniciar el hijo.
    pid: int | None = None
    # Detalle de error cuando no se puede iniciar o supervisar el proceso.
    error_message: str | None = None
    # Canales se mantienen separados para que la CLI pueda mostrar cada uno.
    stdout: str = ""
    stderr: str = ""
    # Señal interna leída por el monitor para asignar CANCELED al terminar.
    cancel_requested: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Convierte los metadatos a tipos que json.dumps puede serializar."""
        # Enum se reemplaza por su texto para que la CLI pueda crear JSON.
        return {
            "id": self.id,
            "command": self.command,
            "status": self.status.value,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "exit_code": self.exit_code,
            "pid": self.pid,
            "error_message": self.error_message,
            "stdout": self.stdout,
            "stderr": self.stderr,
        }