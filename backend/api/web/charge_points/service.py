from typing import Dict

from propan import apply_types, Depends, Context
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.exceptions import NotFound
from api.web.charge_points.models import ChargePoint
from core.models import get_session


@apply_types
async def update_charge_point(
        charge_point_id: str,
        payload: Dict,
        session: AsyncSession = Context()
):
    await session.execute(
        update(ChargePoint) \
            .where(ChargePoint.id == charge_point_id) \
            .values(**payload)
    )


@apply_types
async def get_charge_point(
        charge_point_id: str,
        session: AsyncSession = Depends(get_session)
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
        raise NotFound(detail=f"The charge point with id: '{charge_point_id}' has not found.")
    return charge_point
