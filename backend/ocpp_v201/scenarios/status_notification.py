from datetime import datetime
from typing import Dict, Any

from loguru import logger
from ocpp.routing import on, after
from ocpp.v201 import call_result
from ocpp.v201.enums import Action, ConnectorStatusType
from propan import apply_types, Depends, Context

from app.web.charge_points import get_charge_point_service
from app.web.connections.service import update_connection
from app.web.connections.views import ConnectionView
from app.web.logs import get_logs_service


@apply_types
async def _on_status_notification(
        timestamp: datetime,
        connector_status: ConnectorStatusType,
        evse_id: int,
        connector_id: int,
        custom_data: Dict[str, Any],
        service: Any = Depends(get_charge_point_service),
        charge_point_id=Context(),
        session: Any = Context()
):
    with logger.contextualize(charge_point_id=charge_point_id, session_id=session.id):
        logger.info(f"Accepted '{Action.StatusNotification}'")
        charge_point = await service.get_charge_point(charge_point_id)
        if service.is_connector_id_common(connector_id):
            data = ConnectionView(status=connector_status)
            await update_connection(charge_point_id, data.model_dump(exclude_unset=True))
            logger.info("Updated entire station status", extra={"status": charge_point.connection.status})
            await session.commit()
            return call_result.StatusNotificationPayload()

        """
        Since we don’t remove EVSEs and stations when the WebSocket connection fails,
        let’s first check if one already exists.
        """
        if not charge_point.has_evse(evse_id):
            evse = await service.create_evse(charge_point_id, evse_id)
        else:
            evse = charge_point.get_evse(charge_point_id, evse_id)

        if not evse.has_connector(connector_id):
            connector = await service.create_connector(evse, connector_id)
        else:
            connector = evse.get_connector(connector_id)

        await connector.apply_status(connector_status)
        await session.commit()
        return call_result.StatusNotificationPayload()


@apply_types
async def _after_status_notification(
        call_unique_id,
        timestamp,
        connector_status,
        evse_id,
        connector_id,
        custom_data,
        service: Any = Depends(get_logs_service),
        charge_point_id=Context()
):
    call_results = await service.find_payloads_by_id(call_unique_id)
    with logger.contextualize(charge_point_id=charge_point_id, call_results=call_results):
        logger.info(f"Post processing '{Action.StatusNotification}'")


class StatusNotificationScenario:

    @on(Action.StatusNotification)
    async def on_status_notification(
            self_,
            timestamp: str,
            connector_status: ConnectorStatusType,
            evse_id: int,
            connector_id: int,
            **kwargs,
    ):
        return await _on_status_notification(
            timestamp=timestamp,
            connector_status=connector_status,
            evse_id=evse_id,
            connector_id=connector_id,
            custom_data=kwargs
        )

    @after(Action.StatusNotification)
    async def after_status_notification(
            self_,
            call_unique_id,
            timestamp: str,
            connector_status: ConnectorStatusType,
            evse_id: int,
            connector_id: int,
            **kwargs,
    ):
        return await _after_status_notification(
            call_unique_id=call_unique_id,
            timestamp=timestamp,
            connector_status=connector_status,
            evse_id=evse_id,
            connector_id=connector_id,
            custom_data=kwargs
        )
