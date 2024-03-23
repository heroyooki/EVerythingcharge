from __future__ import annotations

import asyncio
from typing import Any, Dict

from fast_depends import Depends
from loguru import logger
from propan import Context
from propan.annotations import ContextRepo

from api.web.charge_points import get_handler, get_charge_point_service
from core.broker import broker, events_exchange, connections_exchange
from core.models import get_contextual_session
from core.settings import (
    EVENTS_QUEUE_NAME,
    NEW_CONNECTION_QUEUE_NAME,
    FORCE_CLOSE_CONNECTION_QUEUE_NAME,
    CHARGE_POINT_ID_HEADER_NAME,
    LOST_CONNECTION_QUEUE_NAME
)
from core.utils import get_id_from_amqp_headers


async def init_local_scope(
        context: ContextRepo,
        charge_point_id=Depends(get_id_from_amqp_headers)
):
    async with get_contextual_session() as session:
        context.set_local("session", session)
        context.set_local("charge_point_id", charge_point_id)


async def init_global_scope(context):
    context.set_global("response_queues", dict())


@broker.handle(EVENTS_QUEUE_NAME, exchange=events_exchange)
async def handle_events(
        payload: str,
        scope=Depends(init_local_scope),
        handler: Any = Depends(get_handler),
        session=Context()
):
    logger.info(f"Accepted payload from the station "
                f"(payload={payload}, "
                f"charge_point_id={handler.charge_point.id}"
                )
    await handler.route_message(payload)
    await session.commit()


@broker.handle(NEW_CONNECTION_QUEUE_NAME, exchange=connections_exchange)
async def accept_new_connection(
        scope=Depends(init_local_scope),
        service: Any = Depends(get_charge_point_service),
        charge_point_id=Context(),
        response_queues: Dict = Context(),
        session=Context()
):
    charge_point = await service.get_charge_point(charge_point_id)
    if not charge_point:
        await broker.publish(
            "[]",
            exchange=connections_exchange,
            routing_key=f"{FORCE_CLOSE_CONNECTION_QUEUE_NAME}.*",
            content_type="text/plain",
            headers={
                CHARGE_POINT_ID_HEADER_NAME: charge_point_id
            }
        )
        logger.info(f"Not found '{charge_point_id}'. Cancelling connection.")
        return
    response_queues[charge_point_id] = asyncio.Queue()
    logger.info(f"Accepted connection "
                f"(charge_point_id={charge_point_id}, "
                f"response_queue={response_queues[charge_point_id]}"
                )

    await session.commit()


@broker.handle(LOST_CONNECTION_QUEUE_NAME, exchange=connections_exchange)
async def process_lost_connection(
        scope=Depends(init_local_scope),
        charge_point_id=Context(),
        response_queues=Context(),
        session=Context()
):
    logger.info(f"Lost connection with {charge_point_id}")
    response_queues.pop(charge_point_id, None)
    await session.commit()
