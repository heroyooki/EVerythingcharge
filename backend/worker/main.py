import asyncio
import json
from uuid import uuid4

import websockets
from loguru import logger
from propan import Context, apply_types, Depends
from propan.annotations import ContextRepo
from propan.brokers.rabbit import RabbitQueue

from core.annotations import (
    TasksRepo,
    ConnectionsExchange,
    EventsExchange,
    AMQPHeaders
)
from core.broker import (
    broker,
    connections_exchange,
    tasks_exchange
)
from core.dependencies import get_id_from_amqp_headers
from core.settings import (
    FORCE_CLOSE_CONNECTION_QUEUE_NAME,
    WS_SERVER_PORT,
    NEW_CONNECTION_QUEUE_NAME,
    EVENTS_QUEUE_NAME,
    LOST_CONNECTION_QUEUE_NAME
)
from worker.protocols import BaseWebSocketServerProtocol
from worker.router import (
    redirect_payload_to_broker,
    redirect_payload_to_websocket
)


@broker.handle(
    RabbitQueue(f"{FORCE_CLOSE_CONNECTION_QUEUE_NAME}.{uuid4().hex}",
                routing_key=f"{FORCE_CLOSE_CONNECTION_QUEUE_NAME}.*",
                auto_delete=True),
    exchange=connections_exchange
)
async def close_websocket_connection(
        charge_point_id=Depends(get_id_from_amqp_headers),
        ws_server=Context()
):
    for connection in ws_server.websockets:
        if charge_point_id == connection.charge_point_id:
            await connection.close()


@broker.handle(uuid4().hex, exchange=tasks_exchange)
async def accept_payload_from_broker(
        payload: str,
        charge_point_id=Depends(get_id_from_amqp_headers)
):
    await redirect_payload_to_websocket(charge_point_id, payload)


@apply_types
async def warn_about_connection(
        routing_key: str,
        exchange: ConnectionsExchange,
        amqp_headers: AMQPHeaders,

):
    await redirect_payload_to_broker(
        payload=json.dumps([]),
        headers=amqp_headers,
        exchange=exchange,
        routing_key=routing_key
    )


@apply_types
async def process_payloads_from_websocket(
        routing_key: str,
        connection: BaseWebSocketServerProtocol,
        exchange: EventsExchange,
        amqp_headers: AMQPHeaders,
):
    while True:
        payload = await connection.recv()

        await redirect_payload_to_broker(
            payload=payload,
            headers=amqp_headers,
            exchange=exchange,
            routing_key=routing_key
        )


@apply_types
async def on_websocket_connect(
        connection: BaseWebSocketServerProtocol,
        path: str,
        context: ContextRepo,
):
    if not connection.subprotocol:
        return await connection.close()

    connection.set_charge_point_id(path)

    with context.scope("charge_point_id", connection.charge_point_id):

        await warn_about_connection(NEW_CONNECTION_QUEUE_NAME)

        try:
            await process_payloads_from_websocket(connection=connection, routing_key=EVENTS_QUEUE_NAME)
        except websockets.exceptions.ConnectionClosedOK:
            await warn_about_connection(LOST_CONNECTION_QUEUE_NAME)


@apply_types
async def main(tasks_repo: TasksRepo, context: ContextRepo):
    server = await websockets.serve(
        lambda connection, path: on_websocket_connect(connection, path),
        '0.0.0.0',
        WS_SERVER_PORT,
        create_protocol=BaseWebSocketServerProtocol,
        subprotocols=['ocpp2.0.1']
    )
    context.set_global("ws_server", server)

    task = asyncio.create_task(broker.start())
    # Save a reference to the result of this function, to avoid a task disappearing mid-execution.
    # The event loop only keeps weak references to tasks.
    tasks_repo.add(task)

    logger.info(f"Start websockets server, listening on {WS_SERVER_PORT} port.")
    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
