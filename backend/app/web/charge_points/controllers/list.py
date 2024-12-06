from typing import Tuple

from fastapi import Depends
from starlette import status

from app.web.charge_points.controllers.router import router
from app.web.charge_points.models import ChargePoint
from app.web.charge_points.service import build_charge_points_query
from app.web.charge_points.views import PaginatedChargePointsView
from app.web.utils import params_extractor, paginate


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
