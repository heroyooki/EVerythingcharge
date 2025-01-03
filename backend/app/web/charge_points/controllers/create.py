from typing import Any

from fastapi import Depends
from starlette import status

from app.web.charge_points.controllers.router import router
from app.web.charge_points.service import create_charge_point
from app.web.charge_points.views import ChargePointView


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ChargePointView
)
async def add_charge_point(charge_point: Any = Depends(create_charge_point)):
    return charge_point
