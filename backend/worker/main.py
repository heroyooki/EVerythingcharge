import asyncio

import websockets
from propan import RabbitBroker, Context
from loguru import logger

from core.settings import (
    MESSAGES_BROKER_URL,
    WS_SERVER_PORT
)
from worker.protocols import BaseWebSocketServerProtocol
from worker.routers import MessagesRouter


router = MessagesRouter()
broker = RabbitBroker(MESSAGES_BROKER_URL)
router.with_broker(broker)

background_tasks = set()


@router.broker.handle(router.worker_queue_name, exchange=router.tasks_exchange)
async def handle_task(body, message=Context()):
    await router.redirect_message_to_websocket(body, message.headers)


async def on_websocket_connect(
        connection: BaseWebSocketServerProtocol,
        path: str
):
    logger.info(f"New charge point connected (path={path})")
    connection.set_charge_point_id(path)
    while True:
        message = await connection.recv()
        logger.info(
            f"Got message from charge point "
            f"(charge_point_id={connection.charge_point_id}, message={message})")
        await router.redirect_message_to_broker(message, connection.charge_point_id)


async def main():
    router.with_ws_server(
        await websockets.serve(
            on_websocket_connect,
            '0.0.0.0',
            WS_SERVER_PORT,
            create_protocol=BaseWebSocketServerProtocol
        )
    )
    logger.info(f"Started websocket server on port {WS_SERVER_PORT}")

    task = asyncio.create_task(broker.start())
    # Save a reference to the result of this function, to avoid a task disappearing mid-execution.
    # The event loop only keeps weak references to tasks.
    background_tasks.add(task)
    logger.info(f"Started broker with handlers: {broker.handlers}")

    await router.ws_server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())

