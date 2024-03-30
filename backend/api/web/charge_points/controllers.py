from typing import Any

from fastapi import Depends
from starlette import status

from api.web.charge_points.service import create_charge_point
from api.web.charge_points.views import SingleChargePointView
from api.web.routing import PrivateAPIRouter

router = PrivateAPIRouter(prefix="/{network_id}/charge_points")


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=SingleChargePointView
)
async def add_charge_point(charge_point: Any = Depends(create_charge_point)):
    return charge_point
