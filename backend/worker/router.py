from typing import Dict, Any

from fast_depends import inject
from loguru import logger
from propan import Context

from core import Settings, EventsExchange, PayloadJsonLoader, PayloadJsonDumper

_ws_server: Any = None
_broker: Any = None


@inject
async def redirect_payload_to_websocket(
        payload: PayloadJsonDumper,
        headers: Dict,
        settings: Settings,
        ws_server=Context(),
):
    async for connection in ws_server.connections:
        if headers[settings.CHARGE_POINT_ID_HEADER_NAME] \
                == connection.charge_point_id:
            await connection.send(payload)


@inject
async def redirect_payload_to_broker(
        payload: PayloadJsonLoader,
        charge_point_id: str,
        settings: Settings,
        exchange: EventsExchange,
        broker=Context(),
):
    logger.info(
        f"Redirecting payload to the broker "
        f"(payload={payload}, "
        f"settings={settings}, "
        f"exchange={exchange})")
    await broker.publish(
        payload,
        exchange=exchange,
        routing_key=settings.EVENTS_QUEUE_NAME,
        headers={
            settings.CHARGE_POINT_ID_HEADER_NAME: charge_point_id
        }
    )
