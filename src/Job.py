"""Importación de compatibilidad para código que usa `src.Job`.

La definición única de las clases vive en `models.py`; este módulo conserva
los nombres de importación usados por algunos consumidores anteriores.
"""

from .models import Job, JobStatus

__all__ = ["Job", "JobStatus"]