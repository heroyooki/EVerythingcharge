import asyncio
from uuid import uuid4

import websockets
from propan import Context, apply_types
from propan.annotations import ContextRepo

from core.annotations import TasksRepo, Settings, Logger
from core.settings import broker, tasks_exchange
from worker.protocols import BaseWebSocketServerProtocol
from worker.router import redirect_payload_to_broker, redirect_payload_to_websocket


@broker.handle(uuid4().hex, exchange=tasks_exchange)
async def accept_payload_from_broker(payload: str, message=Context()):
    await redirect_payload_to_websocket(payload=payload, headers=message.headers)


@apply_types
async def process_new_connection(
        charge_point_id: str,
        context: ContextRepo,
        settings: Settings,
        logger: Logger
):
    logger.info(f"Accepted connection from {charge_point_id}")

    with context.scope("routing_key", settings.NEW_CONNECTION_QUEUE_NAME):
        await redirect_payload_to_broker(
            payload="[]",
            charge_point_id=charge_point_id
        )


@apply_types
async def process_lost_connection(
        charge_point_id: str,
        context: ContextRepo,
        settings: Settings
):
    with context.scope("routing_key", settings.LOST_CONNECTION_QUEUE_NAME):
        await redirect_payload_to_broker(
            payload="[]",
            charge_point_id=charge_point_id
        )


@apply_types
async def process_payloads_from_websocket(
        connection: BaseWebSocketServerProtocol,
        context: ContextRepo,
        settings: Settings
):
    while True:
        payload = await connection.recv()
        with context.scope("routing_key", settings.EVENTS_QUEUE_NAME):
            await redirect_payload_to_broker(
                payload=payload,
                charge_point_id=connection.charge_point_id
            )


async def on_websocket_connect(connection: BaseWebSocketServerProtocol, path: str):
    connection.set_charge_point_id(path)
    await process_new_connection(charge_point_id=connection.charge_point_id)
    try:
        await process_payloads_from_websocket(connection=connection)
    except websockets.exceptions.ConnectionClosedOK:
        await process_lost_connection(charge_point_id=connection.charge_point_id)


@apply_types
async def main(
        settings: Settings,
        tasks_repo: TasksRepo,
        context: ContextRepo,
        logger: Logger,
        broker=Context(),
):
    server = await websockets.serve(
        on_websocket_connect,
        '0.0.0.0',
        settings.WS_SERVER_PORT,
        create_protocol=BaseWebSocketServerProtocol
    )
    context.set_global("ws_server", server)

    task = asyncio.create_task(broker.start())
    # Save a reference to the result of this function, to avoid a task disappearing mid-execution.
    # The event loop only keeps weak references to tasks.
    tasks_repo.add(task)

    logger.info(f"Start websockets server, listening on {settings.WS_SERVER_PORT} port.")
    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
