from typing import Any, Dict

from loguru import logger
from ocpp.routing import on
from ocpp.v201 import call_result
from ocpp.v201.enums import RegistrationStatusType, Action
from propan import apply_types, Depends

from api.web.charge_points import get_charge_point_service
from core.annotations import Settings
from core.utils import get_formatted_utc


class BootNotificationScenario:

    @apply_types
    @on(Action.BootNotification)
    async def on_boot_notification(
            this,
            settings: Settings,
            utc_datetime: str = Depends(get_formatted_utc),
            charging_station: Dict = Depends(lambda charging_station: charging_station),
            reason: str = Depends(lambda reason: reason),
            service: Any = Depends(get_charge_point_service),
            **kwargs
    ):
        logger.info(
            f"Accepted '{Action.BootNotification}' "
            f"(charging_station={charging_station}, "
            f"reason={reason}, "
            f"kwargs={kwargs})"
        )
        await service.update_charge_point(
            charge_point_id=this.id,
            payload=dict(
                vendor=charging_station.get("vendor_name"),
                model=charging_station.get("model"),
            )
        )
        return call_result.BootNotificationPayload(
            current_time=utc_datetime,
            interval=settings.HEARTBEAT_INTERVAL,
            status=RegistrationStatusType.accepted,
        )
