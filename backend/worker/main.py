import asyncio
from uuid import uuid4

import websockets
from fast_depends import inject
from loguru import logger
from propan import Context

from core import tasks_exchange, broker, Settings, settings, JSONLoader, TasksRepo
from worker.protocols import BaseWebSocketServerProtocol
from worker.routers import Router


@broker.handle(
    f"{settings.TASKS_EXCHANGE_NAME}.{uuid4().hex}",
    exchange=tasks_exchange
)
async def accept_message_from_broker(
        body: JSONLoader,
        router: Router,
        message=Context()
):
    await router.redirect_message_to_websocket(body, message.headers)


@inject
async def on_websocket_connect(
        connection: BaseWebSocketServerProtocol,
        path: str,
        router: Router
):
    connection.set_charge_point_id(path)
    while True:
        message = await connection.recv()
        await router.redirect_message_to_broker(
            message,
            connection.charge_point_id
        )


@inject
async def main(
        router: Router,
        settings: Settings,
        tasks_repo: TasksRepo,
        broker=Context()
):
    server = await websockets.serve(
        on_websocket_connect,
        '0.0.0.0',
        settings.WS_SERVER_PORT,
        create_protocol=BaseWebSocketServerProtocol,
        logger=logger
    )
    router.with_ws_server(server) \
        .with_broker(broker)

    task = asyncio.create_task(router.broker.start())
    # Save a reference to the result of this function, to avoid a task disappearing mid-execution.
    # The event loop only keeps weak references to tasks.
    tasks_repo.add(task)

    # Ensure the router has running broker
    broker_starting_timeout = 15  # seconds
    for _ in range(broker_starting_timeout):
        if router.broker.started:
            break
        else:
            await asyncio.sleep(1)

    await router.ws_server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
