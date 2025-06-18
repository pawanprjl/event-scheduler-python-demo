import asyncio
from typing import AsyncGenerator

from loguru import logger

from app.events.event import Event


class EventHandler:
    """Handles events in an asynchronous queue."""

    def __init__(self, max_queue_size: int = 1000):
        self._running = False
        self._queue = asyncio.Queue(maxsize=max_queue_size)
        self._startup_event = asyncio.Event()

    def start(self):
        """Start the event handler."""
        self._running = True
        self._startup_event.set()
        logger.info("Event handler started")

    def stop(self):
        """Stop the event handler."""
        self._running = False
        self._startup_event.clear()
        logger.info("Event handler stopped")

    async def wait_for_startup(self, timeout: float = 5.0):
        """Wait for the event handler to be ready."""
        try:
            await asyncio.wait_for(self._startup_event.wait(), timeout=timeout)
        except asyncio.TimeoutError:
            raise RuntimeError("Event handler failed to start within timeout")

    async def emit(self, event: Event):
        """Emit an event to the queue."""
        if not self._running:
            logger.warning(
                f"Event handler not running, cannot emit event: {event.type.value}"
            )
            return

        try:
            await self._queue.put(event)
            logger.debug(
                f"Event emitted: {event.type.value} (correlation_id: {event.correlation_id})"
            )
        except asyncio.QueueFull:
            logger.error(f"Event queue is full, dropping event: {event.type.value}")
        except Exception as e:
            logger.error(f"Error emitting event {event.type.value}: {e}", exc_info=True)

    async def listen(self) -> AsyncGenerator[Event, None]:
        """
        Generator that yields events from the queue.
        """
        if not self._running:
            self.start()

        try:
            while self._running:
                try:
                    event = await asyncio.wait_for(self._queue.get(), timeout=1.0)
                    yield event
                    self._queue.task_done()
                except asyncio.TimeoutError:
                    continue  # No events in the queue, continue listening
                except asyncio.CancelledError:
                    logger.info("Event listener cancelled, stopping...")
                    break
        except Exception as e:
            logger.error(f"Error in event listener: {e}", exc_info=True)
        finally:
            self._running = False
            logger.info("Event listener has stopped.")
