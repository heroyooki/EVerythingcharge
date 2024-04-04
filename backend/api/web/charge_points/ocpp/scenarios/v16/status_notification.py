from typing import Any

from loguru import logger
from ocpp.routing import on
from ocpp.v16 import call_result
from ocpp.v16.enums import Action, ChargePointErrorCode, ChargePointStatus
from propan import Context
from propan import apply_types, Depends

from api.web.charge_points import get_charge_point_service
from api.web.charge_points.views import UpdateChargePointPayloadView
from api.web.sse import get_sse_publisher


class StatusNotificationScenario:

    @apply_types
    @on(Action.StatusNotification)
    async def on_status_notification(
            self_,
            connector_id: int = Depends(lambda connector_id: connector_id),
            error_code: ChargePointErrorCode = Depends(lambda error_code: error_code),
            sse_publisher: Any = Depends(get_sse_publisher),
            status: ChargePointStatus = Depends(lambda status: status),
            service: Any = Depends(get_charge_point_service),
            session=Context(),
            **kwargs
    ):
        logger.info(
            f"Accepted '{Action.StatusNotification}' "
            f"(connector_id={connector_id}, "
            f"error_code={error_code}, "
            f"status={status}, "
            f"charge_point_id={self_.id}, "
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

        await session.commit()
        await sse_publisher.charge_point_publisher.publish(self_.charge_point)

        return call_result.StatusNotificationPayload()
