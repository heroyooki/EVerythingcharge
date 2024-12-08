import asyncio
import uuid
from dataclasses import asdict

from loguru import logger
from ocpp.charge_point import ChargePoint as cp, snake_to_camel_case, remove_nones, camel_to_snake_case
from ocpp.messages import Call, validate_payload, MessageType
from ocpp.routing import create_route_map
from propan import Depends
from propan import apply_types, Context

from app.web.charge_points.models import ChargePoint
from app.web.exceptions.forbidden import ChargePointIsWaitingForAnotherResponse
from core.annotations import TasksExchange
from core.dependencies import get_settings

locks = {}
locks_lock = asyncio.Lock()


async def get_lock(entity_id):
    async with locks_lock:
        if entity_id in locks:
            raise ChargePointIsWaitingForAnotherResponse(
                detail="Charge point is waiting for another response."
            )
        locks[entity_id] = asyncio.Lock()
        return locks[entity_id]


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

    async def call(self, payload, suppress=True, unique_id=None):
        """
        Send Call message to client and return payload of response.

        The given payload is transformed into a Call object by looking at the
        type of the payload. A payload of type BootNotificationPayload will
        turn in a Call with Action BootNotification, a HeartbeatPayload will
        result in a Call with Action Heartbeat etc.

        A timeout is raised when no response has arrived before expiring of
        the configured timeout.

        When waiting for a response no other Call message can be send. So this
        function will wait before response arrives or response timeout has
        expired. This is in line the OCPP specification

        Suppress is used to maintain backwards compatibility. When set to True,
        if response is a CallError, then this call will be suppressed. When
        set to False, an exception will be raised for users to handle this
        CallError.

        """
        camel_case_payload = snake_to_camel_case(asdict(payload))

        unique_id = (
            unique_id if unique_id is not None else str(self._unique_id_generator())
        )

        call = Call(
            unique_id=unique_id,
            action=payload.__class__.__name__[:-7],
            payload=remove_nones(camel_case_payload),
        )

        validate_payload(call, self._ocpp_version)

        # The instance may be utilized by multiple users. So, lets lock the 'Call' on the id level.
        lock = await get_lock(self.id)
        async with lock:
            await self._send(call.to_json())
            try:
                response = await self._get_specific_response(
                    call.unique_id, self._response_timeout
                )
            except asyncio.TimeoutError:
                raise asyncio.TimeoutError(
                    f"Waited {self._response_timeout}s for response on "
                    f"{call.to_json()}."
                )

        if response.message_type_id == MessageType.CallError:
            logger.warning("Received a CALLError: %s'", response)
            if suppress:
                return
            raise response.to_exception()
        else:
            response.action = call.action
            validate_payload(response, self._ocpp_version)

        snake_case_payload = camel_to_snake_case(response.payload)
        # Create the correct Payload instance based on the received payload. If
        # this method is called with a call.BootNotificationPayload, then it
        # will create a call_result.BootNotificationPayload. If this method is
        # called with a call.HeartbeatPayload, then it will create a
        # call_result.HeartbeatPayload etc.
        cls = getattr(self._call_result, payload.__class__.__name__)  # noqa
        try:
            return cls(**snake_case_payload)
        finally:
            async with locks_lock:
                del locks[self.id]

    # To prevent default behavior because we dont need it
    async def start(self_):
        pass
