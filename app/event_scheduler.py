import asyncio
import signal
from loguru import logger

from app.job_manager import JobManager
from app.events import Event, EventType, EventHandler


class EventScheduler:
    def __init__(self):
        self.running = False
        self._shutdown_event = asyncio.Event()
        self.event_handler = EventHandler()
        self.job_manager = JobManager(self.event_handler)

    def setup_signal_handlers(self):
        # Setup signal handlers for graceful shutdown
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(
            signal.SIGINT, lambda: asyncio.create_task(self.shutdown())
        )
        loop.add_signal_handler(
            signal.SIGTERM, lambda: asyncio.create_task(self.shutdown())
        )

    async def process_events(self):
        """
        Process events from the event handler.
        """
        async for event in self.event_handler.listen():
            logger.debug(
                f"Processing event: {event.type.value} (correlation_id: {event.correlation_id})"
            )

    async def shutdown(self):
        if not self.running:
            logger.warning("Application is not running, nothing to shut down.")
            return

        logger.info("Initiating gracious shutdown...")
        self.running = False

        # Emit shutdown event
        await self.event_handler.emit(Event.create(EventType.SHUTDOWN_REQUESTED))

        # Perform any necessary cleanup here
        self.job_manager.shutdown()

        # Set shutdown event
        self._shutdown_event.set()

        logger.info("Shutdown complete.")

    async def run(self):
        try:
            logger.info("Application is starting...")
            self.running = True

            # Setup signal handlers
            self.setup_signal_handlers()

            # Start the job manager
            self.job_manager.startup()

            # Start processing events
            event_task = asyncio.create_task(self.process_events())

            logger.info("✅ Application is running. Press Ctrl+C to stop.")

            # Wait for the shutdown signal
            await self._shutdown_event.wait()

            # Cancel the event processing task on shutdown
            event_task.cancel()

            try:
                await event_task
            except asyncio.CancelledError:
                pass

        except Exception as e:
            logger.error(
                f"An error occurred while starting the application: {e}", exc_info=True
            )
            self.running = False
            raise e
        finally:
            logger.info("Application has finished running.")
