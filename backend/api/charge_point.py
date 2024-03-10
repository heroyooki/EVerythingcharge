import asyncio
import uuid

from ocpp.routing import create_route_map
from ocpp.v16 import ChargePoint as cp
from propan import Context, apply_types

from core.annotations import Settings, TasksExchange, AMQPHeaders
from rest.charge_points.scenarios import BootNotificationScenario


class OCPP16ChargePoint(
    cp,
    BootNotificationScenario
):
    """
    Using 'this' instead of 'self':
    https://github.com/Lancetnik/FastDepends/issues/37#issuecomment-1854732858
    """
    _ocpp_version = "1.6"

    @apply_types
    def __init__(
            this,
            charge_point_id: str,
            settings: Settings,
            response_queues=Context()
    ):
        this.id = charge_point_id
        this._call_lock = asyncio.Lock()
        this._unique_id_generator = uuid.uuid4
        this._response_queue = response_queues[this.id]
        this._response_timeout = settings.RESPONSE_TIMEOUT
        this.route_map = create_route_map(this)

    @apply_types
    async def _send(
            this,
            payload,
            exchange: TasksExchange,
            amqp_headers: AMQPHeaders,
            broker=Context()
    ):
        await broker.publish(
            payload,
            exchange=exchange,
            routing_key="",
            content_type="text/plain",
            headers=amqp_headers
        )

    async def start(this):
        pass
