from typing import List, Any

from loguru import logger
from ocpp.routing import on
from ocpp.v201 import call_result
from ocpp.v201.datatypes import EventDataType
from ocpp.v201.enums import Action, EventTriggerType, ConnectorVariableName, PhysicalComponentName
from propan import apply_types, Depends

from app.web.charge_points import get_charge_point_service
from app.web.charge_points.views import UpdateChargePointPayloadView


class NotifyEventScenario:

    def is_status_notification_alternative(self, data: EventDataType, connector_id: Any):
        """
         Instead of a StatusNotificationRequest a Charging Station can send a
         NotifyEventRequest with trigger = Delta for component.name = "Connector"
         and the EVSE number in evse.id and the connector number in evse.connectorId,
         and variable = "AvailabilityState" with the value of the new status to the CSMS.
        :param data:
        :param connector_id:
        :return:
        """
        return EventTriggerType(data.trigger) is EventTriggerType.delta and \
               PhysicalComponentName(data.component.name) is PhysicalComponentName.connector and \
               isinstance(connector_id, int) and \
               ConnectorVariableName(data.variable.name) is ConnectorVariableName.availability_state

    @apply_types
    @on(Action.NotifyEvent)
    async def on_notify_event(
            self_,
            generated_at: str,
            seq_no: int,
            event_data: List[EventDataType],
            service: Any = Depends(get_charge_point_service)
    ):
        """
        :param generated_at:
        :param seq_no:
        :param event_data:
        :return:
        """
        logger.info(
            f"Accepted '{Action.NotifyEvent}' "
            f"generated_at={generated_at},"
            f"seq_no={seq_no},"
            f"event_data={event_data})"
        )

        for data in event_data:
            connector_id = data.component.evse.connector_id
            connector_status = data.actual_value

            if self_.is_status_notification_alternative(data, connector_id):

                payload = UpdateChargePointPayloadView(
                    status=connector_status
                )
                if not connector_id:
                    payload.evse_id = data.component.evse.id
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
            return call_result.NotifyEventPayload()
