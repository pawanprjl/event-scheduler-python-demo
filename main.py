import asyncio
import logging
import sys

from loguru import logger

from app.event_scheduler import EventScheduler
from app.config import settings


# Configure logger
logger.remove()
logger.add(
    sink=sys.stdout,
    level=settings.LOG_LEVEL,
)


async def main():
    logger.info("Starting the scheduler application...")

    app = EventScheduler()
    await app.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Scheduler application stopped by user.")
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        sys.exit(1)
