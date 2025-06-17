from enum import Enum


class EventType(Enum):
    """
    Event types for the application.
    """

    JOB_STARTED = "job_started"
    JOB_COMPLETED = "job_completed"
    JOB_FAILED = "job_failed"
    PROCESS_COMPANY = "process_company"
    COMPANY_PROCESSED = "company_processed"
    COMPANY_FAILED = "company_failed"
    SHUTDOWN_REQUESTED = "shutdown_requested"
