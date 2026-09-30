from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

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
    command: List[str]
    status: JobStatus = JobStatus.QUEUED
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    exit_code: Optional[int] = None
    pid: Optional[int] = None  # Para el compañero que implemente fork/Popen (RF-04)
    error_message: Optional[str] = None

    def to_dict(self) -> dict:
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