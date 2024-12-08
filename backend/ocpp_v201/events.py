import asyncio
import json
from typing import Any, Dict

from loguru import logger
from propan import Context, Depends
from propan.annotations import ContextRepo
from sqlalchemy.ext.asyncio import AsyncSession

from app.web.charge_points import get_charge_point_service
from app.web.exceptions import NotFound
from core.broker import broker, events_exchange, connections_exchange
from core.dependencies import get_id_from_amqp_headers
from core.models import get_contextual_session
from core.settings import (
    EVENTS_QUEUE_NAME,
    NEW_CONNECTION_QUEUE_NAME,
    FORCE_CLOSE_CONNECTION_QUEUE_NAME,
    CHARGE_POINT_ID_HEADER_NAME,
    LOST_CONNECTION_QUEUE_NAME
)
from ocpp_v201.handlers import OCPP201Handler, get_handler


async def init_local_scope(
        context: ContextRepo,
        charge_point_id: str = Depends(get_id_from_amqp_headers)
):
    async with get_contextual_session() as session:
        context.set_local("session", session)
        context.set_local("charge_point_id", charge_point_id)


async def init_global_scope(context):
    # The part of the RPC approcah.
    context.set_global("response_queues", dict())
    context.set_global("get_ocpp_handler", get_handler)


@broker.handle(EVENTS_QUEUE_NAME, exchange=events_exchange)
async def handle_events(
        payload: str,
        _=Depends(init_local_scope),
        charge_point_id: str = Context(),
        get_ocpp_handler: Any = Context()
):
    logger.info(f"Accepted payload", extra={"charge_point_id": charge_point_id, "payload": payload})
    handler: OCPP201Handler = await get_ocpp_handler(charge_point_id)
    await handler.route_message(payload)


@broker.handle(NEW_CONNECTION_QUEUE_NAME, exchange=connections_exchange)
async def accept_new_connection(
        _=Depends(init_local_scope),
        service: Any = Depends(get_charge_point_service),
        charge_point_id: str = Depends(get_id_from_amqp_headers),
        response_queues: Dict = Context(),
        session: AsyncSession = Context()
):
    with logger.contextualize(charge_point_id=charge_point_id):
        try:
            await service.get_charge_point_or_404(charge_point_id)
        except NotFound:
            await broker.publish(
                json.dumps([]),
                exchange=connections_exchange,
                routing_key=f"{FORCE_CLOSE_CONNECTION_QUEUE_NAME}.*",
                content_type="text/plain",
                headers={
                    CHARGE_POINT_ID_HEADER_NAME: charge_point_id
                }
            )
            logger.info(f"Cancelling connection")
        else:
            response_queues[charge_point_id] = asyncio.Queue()
            await service.mark_charge_point_as_connected(charge_point_id)
            logger.info(f"Accepted connection")

    await session.commit()


@broker.handle(LOST_CONNECTION_QUEUE_NAME, exchange=connections_exchange)
async def process_lost_connection(
        _=Depends(init_local_scope),
        service: Any = Depends(get_charge_point_service),
        charge_point_id=Depends(get_id_from_amqp_headers),
        response_queues: Dict = Context(),
        session: AsyncSession = Context()
):
    with logger.contextualize(charge_point_id=charge_point_id):
        response_queues.pop(charge_point_id, None)
        await service.mark_charge_point_as_disconnected(charge_point_id)
        await session.commit()
        logger.info(f"Lost connection")
