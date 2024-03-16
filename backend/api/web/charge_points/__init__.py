from __future__ import annotations

from typing import Any

from propan import apply_types, Depends

from api.web.charge_points.handlers.v16 import OCPP16Handler
from api.web.charge_points.handlers.v201 import OCPP201Handler
from api.web.charge_points.services import get_charge_point


@apply_types
async def get_handler(charge_point: Any = Depends(get_charge_point)):
    return {
        "1.6": OCPP16Handler,
        "2.0.1": OCPP201Handler
    }[charge_point.ocpp_version](charge_point.id)
