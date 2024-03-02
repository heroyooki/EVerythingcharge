from uuid import uuid4

from core.settings import (
    CHARGE_POINT_ID_HEADER_NAME,
    EVENTS_EXCHANGE_NAME,
    TASKS_EXCHANGE_NAME
)

from propan.brokers.rabbit import (
    RabbitExchange,
    ExchangeType
)


class MessagesRouter:

    worker_queue_name = f"{TASKS_EXCHANGE_NAME}.{uuid4().hex}"

    events_exchange = RabbitExchange(
        EVENTS_EXCHANGE_NAME,
        auto_delete=True
    )

    tasks_exchange = RabbitExchange(
        TASKS_EXCHANGE_NAME,
        auto_delete=True,
        type=ExchangeType.FANOUT
    )

    def __init__(self, ws_server=None, broker=None):
        self.ws_server = ws_server
        self.broker = broker

    def with_ws_server(self, ws_server):
        self.ws_server = ws_server

    def with_broker(self, broker):
        self.broker = broker

    async def redirect_message_to_websocket(self, body, headers):
        async for connection in self.ws_server.connections:
            if headers[CHARGE_POINT_ID_HEADER_NAME] == connection.charge_point_id:
                await connection.send(body)

    async def redirect_message_to_broker(self, message, charge_point_id):
        await self.broker.publish(
            message,
            exchange=self.events_exchange,
            headers={CHARGE_POINT_ID_HEADER_NAME: charge_point_id}
        )
