from typing import Any, Tuple

from fastapi import Depends
from starlette import status

from api.web.charge_points.models import ChargePoint
from api.web.charge_points.service import create_charge_point, build_charge_points_query
from api.web.charge_points.views import SingleChargePointView, PaginatedChargePointsView
from api.web.routing import PrivateAPIRouter
from api.web.utils import paginate, params_extractor

router = PrivateAPIRouter(prefix="/{network_id}/charge_points")


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedChargePointsView
)
async def list_charge_points(
        network_id: str,
        params: Tuple = Depends(params_extractor)
) -> PaginatedChargePointsView:
    items, pagination = await paginate(
        build_charge_points_query,
        params,
        extra_criterias=[ChargePoint.network_id == network_id]
    )
    return PaginatedChargePointsView(items=items, pagination=pagination)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=SingleChargePointView
)
async def add_charge_point(charge_point: Any = Depends(create_charge_point)):
    return charge_point
