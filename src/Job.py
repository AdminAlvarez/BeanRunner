# job.py

from enum import Enum
from datetime import datetime
import uuid


class JobStatus(Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELED = "CANCELED"


class Job:

    def __init__(self, command):
        self.id = str(uuid.uuid4())
        self.command = command

        self.status = JobStatus.QUEUED

        self.pid = None

        self.created_at = datetime.now()
        self.started_at = None
        self.finished_at = None

        self.exit_code = None

        self.stdout = ""
        self.stderr = ""

        self.error_message = None