from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class JobStatus(str, Enum):
    """Ciclo de vida oficial del trabajo según RF-06."""

    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELED = "CANCELED"


@dataclass
class Job:
    """Estructura de metadatos del trabajo."""

    id: str
    command: list[str]
    status: JobStatus = JobStatus.QUEUED
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    started_at: str | None = None
    finished_at: str | None = None
    exit_code: int | None = None
    pid: int | None = None
    error_message: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Soporte para serialización/persistencia (RF-12)."""
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
        }