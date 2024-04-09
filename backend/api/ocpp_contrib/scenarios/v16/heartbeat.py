from typing import Any

from loguru import logger
from ocpp.routing import on
from ocpp.v16 import call_result
from ocpp.v16.enums import Action, ChargePointStatus
from propan import Depends, apply_types

from api.web.charge_points import get_charge_point_service
from api.web.charge_points.views import UpdateChargePointPayloadView
from core.utils import get_formatted_utc


class HeartbeatScenario:

    @apply_types
    @on(Action.Heartbeat)
    async def on_heartbeat(
            self_,
            utc_datetime: str = Depends(get_formatted_utc),
            service: Any = Depends(get_charge_point_service)
    ):
        logger.info(
            f"Accepted '{Action.Heartbeat}' "
            f"(charge_point_id={self_.id})"
        )

        payload = UpdateChargePointPayloadView(
            status=ChargePointStatus.available
        )
        await service.update_charge_point(
            charge_point_id=self_.id,
            payload=payload.dict(exclude_unset=True)
        )

        return call_result.HeartbeatPayload(current_time=utc_datetime)
