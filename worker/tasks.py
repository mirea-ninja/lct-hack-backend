from __future__ import annotations

import asyncio
from loguru import logger

from worker import app


async def ping():
    logger.info("ping")


@app.task
def ping_task():
    logger.trace('Попытка выполнить задачу ping')
    event_loop = asyncio.get_event_loop()

    event_loop.run_until_complete(ping())
