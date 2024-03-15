from __future__ import annotations

from propan import apply_types, Depends

from api.web.charge_points.handlers.v16 import OCPP16Handler
from api.web.charge_points.handlers.v201 import OCPP201Handler
from core.annotations import get_id_from_headers


@apply_types
async def get_handler(charge_point_id: str = Depends(get_id_from_headers)):
    # Get charge point model here and refer to the field "ocpp_version"
    ocpp_version = "1.6"
    handler_classes = (OCPP16Handler, OCPP201Handler)
    for handler_class in handler_classes:
        handler = handler_class(charge_point_id)
        if handler._ocpp_version == ocpp_version:
            return handler
