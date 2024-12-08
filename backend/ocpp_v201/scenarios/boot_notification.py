from traceback import format_exc
from typing import Dict, Any

import arrow
from loguru import logger
from ocpp.routing import on
from ocpp.v201 import call_result
from ocpp.v201.enums import (
    Action, BootReasonType, RegistrationStatusType
)
from propan import apply_types, Depends, Context
from sqlalchemy.exc import TimeoutError, InterfaceError

from app.web.charge_points import get_charge_point_service
from app.web.charge_points.views import (
    UpdateChargePointPayloadView
)
from app.web.connections.views import ConnectionView
from core.dependencies import get_settings


@apply_types
async def _on_boot_notification(
        data: Dict,
        reason: BootReasonType,
        custom_data: Dict,
        service: Any = Depends(get_charge_point_service),
        settings: Any = Depends(get_settings),
        charge_point_id=Context(),
        session: Any = Context()
):
    status = RegistrationStatusType.accepted

    with logger.contextualize(charge_point_id=charge_point_id):
        logger.info(f"Accepted '{Action.BootNotification}'")

        try:
            connection_data = ConnectionView(reason=reason, custom_data=custom_data)
            logger.info("Updating connection", data=connection_data.model_dump(exclude_unset=True))
            await service.update_connection(
                charge_point_id=charge_point_id,
                payload=connection_data.model_dump(exclude_unset=True),
            )

            charge_point_data = UpdateChargePointPayloadView(**data)
            logger.info("Updating charge point", data=charge_point_data.model_dump(exclude_unset=True))
            await service.update_charge_point(
                charge_point_id=charge_point_id,
                payload=charge_point_data.model_dump(exclude_unset=True),
            )
            await session.commit()
        except (TimeoutError, InterfaceError):
            # In case of DB issues, make station to connect later.
            await session.rollback()
            logger.error(f"Failed to accept '{Action.BootNotification}' due to conections pool issue",
                         data={"error": format_exc()})
            status = RegistrationStatusType.pending
        except Exception:
            # This is an unrecognized problem, so lets deny station to connect, until to address it.
            await session.rollback()
            logger.error(f"Failed to accept '{Action.BootNotification}' due to unrecognized error",
                         data={"error": format_exc()})
            status = RegistrationStatusType.rejected
        finally:
            return call_result.BootNotificationPayload(
                current_time=arrow.utcnow().datetime.strftime(settings.UTC_DATETIME_FORMAT),
                interval=settings.HEARTBEAT_INTERVAL,
                status=status
            )


class BootNotificationScenario:

    @on(Action.BootNotification)
    async def on_boot_notification(
            self,
            charging_station: Dict,
            reason: str,
            **kwargs
    ):
        return await _on_boot_notification(
            charge_point_id=self.id,
            data=charging_station,
            reason=reason,
            custom_data=kwargs
        )
