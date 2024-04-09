from fastapi import Depends
from starlette import status

from api.web.charge_points.controllers.router import router
from api.web.charge_points.models import ChargePoint
from api.web.charge_points.service import get_charge_point_or_404
from api.web.charge_points.views import ChargePointView


@router.get(
    "/{charge_point_id}",
    status_code=status.HTTP_200_OK,
    response_model=ChargePointView
)
async def receive_charge_point(charge_point: ChargePoint = Depends(get_charge_point_or_404)):
    return charge_point
