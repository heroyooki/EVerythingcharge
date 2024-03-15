from __future__ import annotations

import asyncio
from typing import Any

from fastapi import FastAPI
from loguru import logger
from propan import apply_types, Depends, Context
from propan.annotations import ContextRepo

from api.web.charge_points import get_handler
from core.annotations import TasksRepo, get_id_from_headers
from core.settings import (
    broker,
    EVENTS_QUEUE_NAME,
    events_exchange,
    NEW_CONNECTION_QUEUE_NAME,
    connections_exchange,
    FORCE_CLOSE_CONNECTION_QUEUE_NAME,
    CHARGE_POINT_ID_HEADER_NAME,
    LOST_CONNECTION_QUEUE_NAME
)

app = FastAPI()


@app.on_event("startup")
@apply_types
async def startup(tasks_repo: TasksRepo, context: ContextRepo):
    task = asyncio.create_task(broker.start())
    # Save a reference to the result of this function, to avoid a task disappearing mid-execution.
    # The event loop only keeps weak references to tasks.
    tasks_repo.add(task)

    context.set_global("response_queues", dict())


@broker.handle(EVENTS_QUEUE_NAME, exchange=events_exchange)
async def handle_events(
        payload: str,
        handler: Any = Depends(get_handler),
):
    logger.info(f"Accepted payload from the station "
                f"(payload={payload}, "
                f"charge_point_id={handler.id}"
                )

    await handler.route_message(payload)


@broker.handle(NEW_CONNECTION_QUEUE_NAME, exchange=connections_exchange)
async def accept_new_connection(
        charge_point_id=Depends(get_id_from_headers),
        response_queues=Context()
):
    response_queues[charge_point_id] = asyncio.Queue()
    logger.info(f"Accepted connection "
                f"(charge_point_id={charge_point_id}, "
                f"response_queue={response_queues[charge_point_id]}"
                )
    if not charge_point_id:
        await broker.publish(
            "[]",
            exchange=connections_exchange,
            routing_key=f"{FORCE_CLOSE_CONNECTION_QUEUE_NAME}.*",
            content_type="text/plain",
            headers={
                CHARGE_POINT_ID_HEADER_NAME: charge_point_id
            }
        )


@broker.handle(LOST_CONNECTION_QUEUE_NAME, exchange=connections_exchange)
async def process_lost_connection(
        charge_point_id=Depends(get_id_from_headers),
        response_queues=Context()
):
    logger.info(f"Lost connection with {charge_point_id}")
    response_queues.pop(charge_point_id, None)
