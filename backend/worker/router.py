from typing import Dict

from propan import Context, apply_types

from core.annotations import (
    Settings,
    EventsExchange,
    Logger
)


@apply_types
async def redirect_payload_to_websocket(
        payload: str,
        headers: Dict,
        settings: Settings,
        ws_server=Context(),
):
    for connection in ws_server.websockets:
        if headers[settings.CHARGE_POINT_ID_HEADER_NAME] \
                == connection.charge_point_id:
            await connection.send(payload)


@apply_types
async def redirect_payload_to_broker(
        payload: str,
        charge_point_id: str,
        settings: Settings,
        exchange: EventsExchange,
        logger: Logger,
        broker=Context(),
        routing_key=Context()
):
    logger.info(
        f"Redirecting payload to the broker "
        f"(payload={payload}, "
        f"settings={settings}, "
        f"exchange={exchange})")
    await broker.publish(
        payload,
        exchange=exchange,
        routing_key=routing_key,
        content_type="text/plain",
        headers={
            settings.CHARGE_POINT_ID_HEADER_NAME: charge_point_id
        }
    )
