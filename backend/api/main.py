from __future__ import annotations

import asyncio

from fast_depends import inject
from fastapi import FastAPI
from propan import Context

from core import settings, broker, events_exchange, JSONLoader, TasksRepo


@broker.handle(settings.EVENTS_QUEUE_NAME, exchange=events_exchange)
async def handle_events(body: JSONLoader, message=Context()):
    pass


app = FastAPI()


@app.on_event("startup")
@inject
async def startup(tasks_repo: TasksRepo):
    task = asyncio.create_task(broker.start())
    # Save a reference to the result of this function, to avoid a task disappearing mid-execution.
    # The event loop only keeps weak references to tasks.
    tasks_repo.add(task)
