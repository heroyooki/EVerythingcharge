from typing import Any

from loguru import logger
from ocpp.routing import on
from ocpp.v16 import call_result
from ocpp.v16.enums import Action, ChargePointErrorCode, ChargePointStatus
from propan import apply_types, Depends

from api.web.charge_points import get_charge_point_service
from api.web.charge_points.views import UpdateChargePointPayloadView


class StatusNotificationScenario:

    @apply_types
    @on(Action.StatusNotification)
    async def on_status_notification(
            self_,
            connector_id: int = Depends(lambda connector_id: connector_id),
            error_code: ChargePointErrorCode = Depends(lambda error_code: error_code),
            status: ChargePointStatus = Depends(lambda status: status),
            service: Any = Depends(get_charge_point_service),
            **kwargs
    ):
        logger.info(
            f"Accepted '{Action.StatusNotification}' "
            f"(connector_id={connector_id}, "
            f"error_code={error_code}, "
            f"status={status}"
            f"kwargs={kwargs})"
        )

        payload = UpdateChargePointPayloadView(
            status=status,
            error_code=error_code
        )
        if not connector_id:
            await service.update_charge_point(
                charge_point_id=self_.id,
                payload=payload.dict(exclude_unset=True)
            )
        else:
            await service.create_or_update_connector(
                charge_point_id=self_.id,
                connector_id=connector_id,
                payload=payload.dict(exclude_unset=True)
            )
        return call_result.StatusNotificationPayload()
