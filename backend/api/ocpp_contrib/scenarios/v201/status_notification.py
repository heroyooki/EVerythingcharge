from typing import Dict, Any

from loguru import logger
from ocpp.routing import on
from ocpp.v201 import call_result
from ocpp.v201.enums import Action, ConnectorStatusType
from propan import apply_types, Depends

from api.web.charge_points import get_charge_point_service
from api.web.charge_points.views import UpdateChargePointPayloadView


class StatusNotificationScenario:

    @apply_types
    @on(Action.StatusNotification)
    async def on_status_notification(
            self_,
            custom_data: Dict[str, Any],
            timestamp: str,
            connector_status: ConnectorStatusType,
            connector_id: int,
            evse_id: int,
            service: Any = Depends(get_charge_point_service)
    ):
        logger.info(
            f"Accepted '{Action.StatusNotification}' "
            f"(connector_id={connector_id}, "
            f"connector_status={connector_status}, "
            f"custom_data={custom_data}, "
            f"timestamp={timestamp}, "
            f"charge_point_id={self_.id}, "
            f"evse_id={evse_id})"
        )
        payload = UpdateChargePointPayloadView(
            status=connector_status
        )
        if not connector_id:
            payload.evse_id = evse_id
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
