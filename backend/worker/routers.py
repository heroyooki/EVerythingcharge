from typing import Annotated

from fast_depends import inject, Depends

from core import Settings, EventsExchange


class MessagesRouter:

    def __init__(self, ws_server=None, broker=None):
        self.ws_server = ws_server
        self.broker = broker

    def with_ws_server(self, ws_server):
        self.ws_server = ws_server
        return self

    def with_broker(self, broker):
        self.broker = broker
        return self

    @inject
    async def redirect_message_to_websocket(
            self,
            body,
            headers,
            settings: Settings
    ):
        async for connection in self.ws_server.connections:
            if headers[settings.CHARGE_POINT_ID_HEADER_NAME] \
                    == connection.charge_point_id:
                await connection.send(body)

    @inject
    async def redirect_message_to_broker(
            self,
            message,
            charge_point_id,
            settings: Settings,
            exchange: EventsExchange
    ):
        await self.broker.publish(
            message,
            exchange=exchange,
            headers={settings.CHARGE_POINT_ID_HEADER_NAME: charge_point_id}
        )


router = MessagesRouter()


async def get_router():
    return router


Router = Annotated[MessagesRouter, Depends(get_router)]
