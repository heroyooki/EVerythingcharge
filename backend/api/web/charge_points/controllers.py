from typing import Any, Tuple

from fastapi import Depends, BackgroundTasks
from sse_starlette.sse import EventSourceResponse
from starlette import status

from api.web.charge_points.models import ChargePoint
from api.web.charge_points.service import create_charge_point, build_charge_points_query
from api.web.charge_points.views import SingleChargePointView, PaginatedChargePointsView
from api.web.routing import PrivateAPIRouter
from api.web.sse import get_sse_publisher, get_observer, get_event_generator
from api.web.utils import paginate, params_extractor

router = PrivateAPIRouter(prefix="/{network_id}/charge_points")
stream_router = PrivateAPIRouter(prefix="/{network_id}")


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
async def add_charge_point(
        background_tasks: BackgroundTasks,
        charge_point: Any = Depends(create_charge_point),
        sse_piblisher: Any = Depends(get_sse_publisher)
):
    background_tasks.add_task(
        sse_piblisher.simple_charge_point_publisher.publish,
        charge_point
    )
    return charge_point


@stream_router.get("/charge_points/stream")
async def listed_stream(
        observer=Depends(get_observer),
        sse_publisher=Depends(get_sse_publisher),
        event_generator=Depends(get_event_generator)
):
    await observer.subscribe(sse_publisher.simple_charge_point_publisher)
    return EventSourceResponse(
        event_generator(observer)
    )
