from __future__ import annotations

from typing import Any

from propan import apply_types, Depends

from api.web.charge_points import service as charge_point_service
from core.utils import get_id_from_amqp_headers


def get_charge_point_service():
    return charge_point_service


@apply_types
async def get_handler(
        charge_point_id: str = Depends(get_id_from_amqp_headers),
        service: Any = Depends(get_charge_point_service),
):
    from api.web.charge_points.ocpp.handlers.v16 import OCPP16Handler
    from api.web.charge_points.ocpp.handlers.v201 import OCPP201Handler

    charge_point = await service.get_charge_point(charge_point_id)

    return {
        "1.6": OCPP16Handler,
        "2.0.1": OCPP201Handler
    }[charge_point.ocpp_version](charge_point)
