import asyncio
from uuid import uuid4

import websockets
from fast_depends import inject
from loguru import logger
from propan import Context
from propan.annotations import ContextRepo

from core import tasks_exchange, broker, Settings, settings, TasksRepo, PayloadJsonDumper
from worker.protocols import BaseWebSocketServerProtocol
from worker.router import redirect_payload_to_broker, redirect_payload_to_websocket


@broker.handle(
    f"{settings.TASKS_EXCHANGE_NAME}.{uuid4().hex}",
    exchange=tasks_exchange
)
async def accept_payload_from_broker(payload: PayloadJsonDumper, message=Context()):
    await redirect_payload_to_websocket(payload=payload, headers=message.headers)


async def on_websocket_connect(connection: BaseWebSocketServerProtocol, path: str):
    connection.set_charge_point_id(path)
    logger.info(f"Accepted connection from {connection.charge_point_id}")

    while True:
        payload = await connection.recv()
        logger.info(f"Received payload from {connection.charge_point_id}: {payload}")
        await redirect_payload_to_broker(payload=payload, charge_point_id=connection.charge_point_id)


@inject
async def main(
        settings: Settings,
        tasks_repo: TasksRepo,
        context: ContextRepo,
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
