import pytest

from app.web.charge_points import get_charge_point_service
from app.web.charge_points.models import ChargePoint

service = get_charge_point_service()


@pytest.mark.asyncio
async def test_create_charge_point(session, charge_point: ChargePoint):
    charge_point = await service.get_charge_point(charge_point.id, session)
    assert not charge_point.connection.is_active
    assert charge_point.connection.status is None
