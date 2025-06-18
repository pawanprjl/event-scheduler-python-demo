from enum import Enum


class EventType(Enum):
    """
    Event types for the application.
    """

    JOB_STARTED = "job_started"
    JOB_COMPLETED = "job_completed"
    JOB_FAILED = "job_failed"
    SHUTDOWN_REQUESTED = "shutdown_requested"
