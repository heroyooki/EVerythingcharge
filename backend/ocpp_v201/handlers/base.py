import asyncio
import uuid

from ocpp.charge_point import ChargePoint as cp
from ocpp.routing import create_route_map
from propan import Depends
from propan import apply_types, Context

from api.web.charge_points.models import ChargePoint
from core.annotations import TasksExchange
from core.dependencies import get_settings


class OCPPHandler(cp):
    """
    Using 'self_' instead of 'self':
    https://github.com/Lancetnik/FastDepends/issues/37#issuecomment-1854732858
    """

    @apply_types
    def __init__(
            self_,
            charge_point: ChargePoint,
            response_queues=Context(),
            settings=Depends(get_settings)
    ):
        self_.id = charge_point.id
        self_.charge_point = charge_point
        self_._call_lock = asyncio.Lock()
        self_._unique_id_generator = uuid.uuid4
        self_._response_queue = response_queues[self_.id]
        self_._response_timeout = settings.RESPONSE_TIMEOUT
        self_.route_map = create_route_map(self_)
        self_.amqp_headers = {
            settings.CHARGE_POINT_ID_HEADER_NAME: charge_point.id
        }

    @apply_types
    async def _send(
            self_,
            payload,
            exchange: TasksExchange,
            broker=Context()
    ):
        await broker.publish(
            payload,
            exchange=exchange,
            routing_key="",
            content_type="text/plain",
            headers=self_.amqp_headers
        )

    # To prevent default behavior because we dont need it
    async def start(self_):
        pass
