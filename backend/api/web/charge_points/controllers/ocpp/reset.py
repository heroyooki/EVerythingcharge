import asyncio
from typing import Dict, Any, Union

from fastapi import Depends
from loguru import logger
from starlette import status

from api.ocpp_contrib.handlers.v16 import OCPP16Handler
from api.ocpp_contrib.handlers.v201 import OCPP201Handler
from api.web.charge_points import get_charge_point_service, get_handler
from api.web.charge_points.controllers.router import router


@router.patch(
    "/{charge_point_id}/reset",
    status_code=status.HTTP_200_OK
)
async def reset_charge_point(
        data: Dict,
        charge_point_id: str,
        service: Any = Depends(get_charge_point_service),
):
    """
    Every status, except 'Rejected' is getting considered as a permission to
        reset statuses to 'Unavailable'.
    If the client received charge_point in the response with 'Unavailable' status, this means
        the operation was accepted by the station.
    """
    handler: Union[OCPP16Handler, OCPP201Handler] = await get_handler(charge_point_id)
    payload = handler.reset_payload_class(**data)

    try:
        response = await handler.call(payload)
    except asyncio.TimeoutError:
        logger.error(f"Timeout for call request exceeded (charge_point_id={charge_point_id})")
        return handler.charge_point

    if not handler.reset_status_class(response.status) is handler.reset_status_class.rejected:
        return await service.drop_statuses(charge_point_id)
    return handler.charge_point
