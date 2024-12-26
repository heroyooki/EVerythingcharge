from typing import Dict, List

from propan import apply_types, Context
from sqlalchemy import select, update, or_, func, String, delete
from sqlalchemy.sql import selectable

from app.web.charge_points.models import (
    ChargePoint,
    Connector,
    Connection,
    EVSE
)
from app.web.connections.service import update_connection
from app.web.connections.views import ConnectionView
from app.web.exceptions import NotFound


async def build_charge_points_query(
        search: str | None = None,
        extra_criterias: List | None = None
) -> selectable:
    criterias = [
        ChargePoint.is_active.is_(True)
    ]
    if extra_criterias:
        criterias.extend(extra_criterias)
    query = select(ChargePoint)
    for criteria in criterias:
        query = query.where(criteria)
    query = query.order_by(ChargePoint.connection.status.asc())
    if search:
        query = query.where(
            or_(
                func.lower(ChargePoint.id).contains(func.lower(search)),
                func.cast(ChargePoint.connection.status, String).ilike(f"{search}%"),
                func.lower(ChargePoint.location).contains(func.lower(search)),
            )
        )
    return query


@apply_types
async def create_charge_point(data: Dict, session=Context()) -> ChargePoint:
    charge_point = ChargePoint(**data)
    session.add(charge_point)
    connection = Connection(master_id=charge_point.id, is_active=False)
    session.add(connection)
    return charge_point


@apply_types
async def get_charge_point(charge_point_id: str, session=Context()) -> ChargePoint | None:
    query = select(ChargePoint).where(ChargePoint.id == charge_point_id)
    result = await session.execute(query)
    charge_point = result.scalars().first()
    return charge_point


@apply_types
async def get_charge_point_or_404(charge_point_id: str) -> ChargePoint:
    charge_point = await get_charge_point(charge_point_id)
    if not charge_point:
        raise NotFound(detail=f"The charge point with id: '{charge_point_id}' has not found.")
    return charge_point


@apply_types
async def delete_charge_points(charge_point_ids: List[str], session=Context()):
    query = delete(ChargePoint).where(ChargePoint.id.in_(charge_point_ids))
    await session.execute(query)


@apply_types
async def update_charge_point(charge_point_id: str, payload: Dict, session=Context()) -> ChargePoint:
    stmt = update(ChargePoint) \
        .where(ChargePoint.id == charge_point_id) \
        .values(**payload) \
        .returning(ChargePoint)
    scalar_result = await session.scalars(stmt)
    results = scalar_result.unique()
    return results.first()


async def mark_charge_point_as_connected(charge_point_id: str):
    data = ConnectionView(is_active=True)
    await update_connection(charge_point_id, data.model_dump(exclude_unset=True))


async def mark_charge_point_as_disconnected(charge_point_id: str):
    data = ConnectionView(is_active=False)
    await update_connection(charge_point_id, data.model_dump(exclude_unset=True))


@apply_types
async def create_connector(evse: EVSE, connector_id: int, session=Context()) -> Connector:
    connector = Connector(evse_id=evse.id, order_id=connector_id)
    session.add(connector)
    connection = Connection(master_id=connector.id, is_active=True)
    session.add(connection)
    return connector


@apply_types
async def create_evse(charge_point_id: str, evse_id: int, session=Context()) -> EVSE:
    evse = EVSE(charge_point_id=charge_point_id, order_id=evse_id)
    session.add(evse)
    return evse


def is_connector_id_common(connector_id: int) -> bool:
    return connector_id == 0
