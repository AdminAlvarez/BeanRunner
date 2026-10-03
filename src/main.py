# models.py
from nanoid import generate

@dataclass(slots=True)
class Job:
    command: list[str]
    # Genera un ID compacto de 10 caracteres por defecto (ej: "V1StGXR8A9")
    id: str = field(default_factory=lambda: generate(size=10))
    status: JobStatus = JobStatus.QUEUED
    ...