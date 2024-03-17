from ocpp.routing import on
from ocpp.v201 import call_result
from ocpp.v201.enums import RegistrationStatusType, Action
from propan import apply_types, Depends

from core.annotations import Settings
from core.utils import get_formatted_utc


class BootNotificationScenario:

    @apply_types
    @on(Action.BootNotification)
    async def on_boot_notification(
            this,
            settings: Settings,
            utc_datetime: str = Depends(get_formatted_utc),
            charging_station=Depends(lambda charging_station: charging_station),
            reason=Depends(lambda reason: reason),
            **kwargs
    ):
        return call_result.BootNotificationPayload(
            current_time=utc_datetime,
            interval=settings.HEARTBEAT_INTERVAL,
            status=RegistrationStatusType.accepted,
        )
