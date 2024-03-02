from websockets.legacy.server import WebSocketServerProtocol


class BaseWebSocketServerProtocol(WebSocketServerProtocol):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.charge_point_id: str | None = None

    def set_charge_point_id(self, path: str):
        self.charge_point_id = path.split("/")[-1].strip("/")
