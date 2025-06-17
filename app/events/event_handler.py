import asyncio
from typing import AsyncGenerator

from loguru import logger

from app.events.event import Event


class EventHandler:
    """Handles events in an asynchronous queue."""

    def __init__(self, max_queue_size: int = 1000):
        self._running = False
        self._queue = asyncio.Queue(maxsize=max_queue_size)

    def stop(self):
        """Stop the event handler."""
        self._running = False

    async def emit(self, event: Event):
        """Emit an event to the queue."""
        if not self._running:
            raise RuntimeError("Event handler is not running.")

        try:
            await self._queue.put(event)
            logger.debug(
                f"Event emitted: {event.type.value} (correlation_id: {event.correlation_id})"
            )
        except asyncio.QueueFull:
            logger.error("Event queue is full, dropping event: {event.type.value}")

    async def listen(self) -> AsyncGenerator[Event, None]:
        """
        Generator that yields events from the queue.
        """
        self._running = True
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
