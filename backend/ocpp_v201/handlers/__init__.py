from __future__ import annotations

from typing import Any

from ocpp.v201 import ChargePoint as ChargePoint201
from propan import apply_types, Depends

from app.web.charge_points import get_charge_point_service
from ocpp_v201.handlers.base import OCPPHandler
from ocpp_v201.scenarios.boot_notification import BootNotificationScenario
from ocpp_v201.scenarios.status_notification import StatusNotificationScenario


class OCPP201Handler(
    OCPPHandler,
    ChargePoint201,

    BootNotificationScenario,
    StatusNotificationScenario
):
    pass


@apply_types
async def get_handler(
        charge_point_id: str,
        service: Any = Depends(get_charge_point_service),
):
    charge_point = await service.get_charge_point(charge_point_id)
    return OCPP201Handler(charge_point)
