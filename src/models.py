from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any
from uuid import uuid4


class JobStatus(StrEnum):
    """Ciclo de vida oficial del trabajo según RF-06."""

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

#maquina de estados finitos
_ALLOWED_TRANSITIONS: dict[JobStatus, frozenset[JobStatus]] = {
    JobStatus.QUEUED: frozenset({JobStatus.RUNNING, JobStatus.CANCELED}),
    JobStatus.RUNNING: frozenset(
        {JobStatus.SUCCEEDED, JobStatus.FAILED, JobStatus.CANCELED}
    ),
    JobStatus.SUCCEEDED: frozenset(),
    JobStatus.FAILED: frozenset(),
    JobStatus.CANCELED: frozenset(),
}


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(slots=True)
class Job:
    """Datos compartidos del trabajo entre runner, executor, manager y CLI."""

    # Argumentos del programa: el primer elemento es el ejecutable.
    command: list[str]
    # UUID usado para buscar el trabajo en los componentes de BeanRunner.
    id: str = field(default_factory=lambda: str(uuid4()))
    # Estado consultado por runner, manager y CLI; inicia antes de ejecutar.
    status: JobStatus = JobStatus.QUEUED
    created_at: datetime = field(default_factory=_utcnow)
    started_at: datetime | None = None
    finished_at: datetime | None = None
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

    @property
    def is_terminal(self) -> bool:
        return not _ALLOWED_TRANSITIONS[self.status]

    def transition_to(self, new_status: JobStatus) -> None:
        """Cambia el estado validando RF-06 y actualiza las marcas de tiempo."""
        if new_status not in _ALLOWED_TRANSITIONS[self.status]:
            raise ValueError(
                f"Transición inválida: {self.status.value} -> {new_status.value}"
            )
        now = _utcnow()
        if new_status is JobStatus.RUNNING:
            self.started_at = now
        elif _ALLOWED_TRANSITIONS[new_status] == frozenset():
            self.finished_at = now
        self.status = new_status

    def to_dict(self, include_output: bool = False) -> dict[str, Any]:
        """Soporte para serialización/persistencia (RF-12)."""
        data: dict[str, Any] = {
            "id": self.id,
            "command": list(self.command),
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
            "exit_code": self.exit_code,
            "pid": self.pid,
            "error_message": self.error_message,
        }
        if include_output:
            data["stdout"] = self.stdout
            data["stderr"] = self.stderr
        return data
