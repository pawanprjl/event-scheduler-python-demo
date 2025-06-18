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
        try:
            async for event in self.event_handler.listen():
                should_continue = await self.job_manager.handle_event(event)
                if not should_continue:
                    logger.info(
                        f"Event processing stopped for event: {event.type.value} (correlation_id: {event.correlation_id})"
                    )
                    break
        except Exception as e:
            logger.error(f"Error in process_events: {e}", exc_info=True)
            raise

    async def startup(self):
        """Initialize and start all components in the correct order."""
        logger.info("Starting up EventScheduler components...")

        # Start the event handler first
        self.event_handler.start()

        # Wait for event handler to be ready
        await self.event_handler.wait_for_startup()

        # Start the job manager
        self.job_manager.startup()

        logger.info("All components started successfully")

    async def shutdown(self):
        if not self.running:
            logger.warning("Application is not running, nothing to shut down.")
            return

        logger.info("Initiating graceful shutdown...")
        self.running = False

        # Emit shutdown event
        try:
            await self.event_handler.emit(Event.create(EventType.SHUTDOWN_REQUESTED))
        except Exception as e:
            logger.warning(f"Could not emit shutdown event: {e}")

        # Perform any necessary cleanup here
        self.job_manager.shutdown()
        self.event_handler.stop()

        # Set shutdown event
        self._shutdown_event.set()

        logger.info("Shutdown complete.")

    async def run(self):
        try:
            logger.info("Application is starting...")
            self.running = True

            # Setup signal handlers
            self.setup_signal_handlers()

            # Initialize all components
            await self.startup()

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
