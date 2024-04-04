from typing import Any

from loguru import logger
from ocpp.routing import on
from ocpp.v201 import call_result
from ocpp.v201.enums import Action, ConnectorStatusType
from propan import Depends, Context, apply_types

from api.web.charge_points import get_charge_point_service
from api.web.charge_points.views import UpdateChargePointPayloadView
from api.web.sse import get_sse_publisher
from core.utils import get_formatted_utc


class HeartbeatScenario:

    @apply_types
    @on(Action.Heartbeat)
    async def on_heartbeat(
            self_,
            utc_datetime: str = Depends(get_formatted_utc),
            service: Any = Depends(get_charge_point_service),
            sse_publisher: Any = Depends(get_sse_publisher),
            session=Context()
    ):
        logger.info(
            f"Accepted '{Action.Heartbeat}' "
            f"(charge_point_id={self_.id})"
        )
        payload = UpdateChargePointPayloadView(
            status=ConnectorStatusType.available
        )
        await service.update_charge_point(
            charge_point_id=self_.id,
            payload=payload.dict(exclude_unset=True)
        )

        await session.commit()
        await sse_publisher.charge_point_publisher.publish(self_.charge_point)

        return call_result.HeartbeatPayload(current_time=utc_datetime)
