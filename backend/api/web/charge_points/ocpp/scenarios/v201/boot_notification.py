from typing import Any, Dict

from loguru import logger
from ocpp.routing import on
from ocpp.v201 import call_result
from ocpp.v201.enums import RegistrationStatusType, Action
from propan import apply_types, Depends

from api.web.charge_points import get_charge_point_service
from api.web.charge_points.views import UpdateChargePointPayloadView
from core.utils import get_formatted_utc, get_settings


class BootNotificationScenario:

    @apply_types
    @on(Action.BootNotification)
    async def on_boot_notification(
            self_,
            utc_datetime: str = Depends(get_formatted_utc),
            charging_station: Dict = Depends(lambda charging_station: charging_station),
            reason: str = Depends(lambda reason: reason),
            service: Any = Depends(get_charge_point_service),
            settings: Any = Depends(get_settings),
            **kwargs
    ):
        logger.info(
            f"Accepted '{Action.BootNotification}' "
            f"(charging_station={charging_station}, "
            f"reason={reason}, "
            f"kwargs={kwargs})"
        )
        payload = UpdateChargePointPayloadView(
            model=charging_station.get("model"),
            vendor=charging_station.get("vendor_name")
        )
        await service.update_charge_point(
            charge_point_id=self_.id,
            payload=payload.dict()
        )
        return call_result.BootNotificationPayload(
            current_time=utc_datetime,
            interval=settings.HEARTBEAT_INTERVAL,
            status=RegistrationStatusType.accepted,
        )
