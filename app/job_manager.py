from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from app.events.event_handler import EventHandler


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

    async def handle_event(self, event):
        logger.debug(
            f"Event handled: {event.type.value} (correlation_id: {event.correlation_id})"
        )
