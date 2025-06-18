from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from app.events import Event, EventType, EventHandler


class JobManager:
    def __init__(self, event_handler: EventHandler):
        self.scheduler = AsyncIOScheduler()
        self.event_handler = event_handler

    def start(self):
        self.scheduler.start()

    def shutdown(self):
        self.scheduler.shutdown(wait=False)

    def add_job(self, func, trigger, **kwargs):
        self.scheduler.add_job(func, trigger, **kwargs)

    def startup(self):
        logger.info("JobManager is starting up...")
        self.start()

    async def handle_event(self, event: Event) -> bool:
        """Handle a single event."""

        logger.debug(
            f"Handling event: {event.type.value} (correlation_id: {event.correlation_id})"
        )

        try:
            if event.type == EventType.JOB_STARTED:
                await self._handle_job_started(event)

            elif event.type == EventType.SHUTDOWN_REQUESTED:
                logger.info("Shutdown requested, stopping event handler")
                return False  # Stop processing events

        except Exception as e:
            logger.error(f"Error handling event: {e}", exc_info=True)

        return True  # Continue processing events

    async def _handle_job_started(self, event: Event):
        """Handle job started event."""
        logger.info(f"Job started: {event.data.get('job_id')}")
