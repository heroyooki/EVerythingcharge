from propan import apply_types, Depends
from sqlalchemy import select

from api.exceptions import NotFound
from api.web.charge_points.models import ChargePoint
from core.annotations import get_id_from_headers
from core.models import get_session


@apply_types
async def get_charge_point(
        charge_point_id=Depends(get_id_from_headers),
        session=Depends(get_session),
) -> ChargePoint | None:
    query = select(ChargePoint).where(ChargePoint.id == charge_point_id)
    result = await session.execute(query)
    charge_point = result.scalars().first()
    return charge_point


@apply_types
async def get_charge_point_or_404(
        charge_point_id,
) -> ChargePoint:
    charge_point = await get_charge_point(charge_point_id)
    if not charge_point:
        raise NotFound(detail="The station is not found.")
    return charge_point