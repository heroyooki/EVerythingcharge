from ocpp.routing import on
from ocpp.v16 import call_result
from ocpp.v16.enums import Action, RegistrationStatus
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
            charge_point_vendor=Depends(lambda charge_point_vendor: charge_point_vendor),
            charge_point_model=Depends(lambda charge_point_model: charge_point_model),
            **kwargs
    ):
        return call_result.BootNotificationPayload(
            current_time=utc_datetime,
            interval=settings.HEARTBEAT_INTERVAL,
            status=RegistrationStatus.accepted,
        )
