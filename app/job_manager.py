from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from app.events import Event, EventType, EventHandler


class JobManager:
    def __init__(self, event_handler: EventHandler):
        self.scheduler = AsyncIOScheduler()
        self.event_handler = event_handler
        self._running = False

    def start(self):
        self.scheduler.start()
        self._running = True

    def shutdown(self):
        self._running = False
        self.scheduler.shutdown(wait=False)

    def add_job(self, func, trigger, **kwargs):
        if not self._running:
            logger.warning("Job manager not running, cannot add job")
            return
        self.scheduler.add_job(func, trigger, **kwargs)

    def startup(self):
        logger.info("JobManager is starting up...")
        self.start()

    async def emit_event(self, event: Event) -> bool:
        """Safely emit an event with error handling."""
        try:
            await self.event_handler.emit(event)
            return True
        except Exception as e:
            logger.error(f"Failed to emit event {event.type.value}: {e}", exc_info=True)
            return False

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

            else:
                logger.warning(f"Unknown event type: {event.type.value}")

        except Exception as e:
            logger.error(f"Error handling event {event.type.value}: {e}", exc_info=True)

        return True  # Continue processing events

    async def _handle_job_started(self, event: Event):
        """Handle job started event."""
        job_id = event.data.get("job_id")
        logger.info(f"Job started: {job_id}")

        # Example: Emit a job completion event after some processing
        # completion_event = Event.create(
        #     EventType.JOB_COMPLETED,
        #     data={'job_id': job_id, 'status': 'completed'},
        #     correlation_id=event.correlation_id
        # )
        # await self.emit_event(completion_event)
