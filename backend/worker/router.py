from typing import Dict

from loguru import logger
from propan import Context, apply_types
from propan.brokers.rabbit import RabbitExchange


@apply_types
async def redirect_payload_to_websocket(
        charge_point_id: str,
        payload: str,
        ws_server=Context(),
):
    for connection in ws_server.websockets:
        if charge_point_id == connection.charge_point_id:
            await connection.send(payload)


@apply_types
async def redirect_payload_to_broker(
        headers: Dict,
        exchange: RabbitExchange,
        routing_key: str,
        payload: str,
        broker=Context(),
):
    logger.info(
        f"Redirecting payload to the broker "
        f"(payload={payload}, "
        f"exchange={exchange})")
    await broker.publish(
        payload,
        exchange=exchange,
        routing_key=routing_key,
        content_type="text/plain",
        headers=headers
    )
