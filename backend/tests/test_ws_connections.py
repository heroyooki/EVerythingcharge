import asyncio

import pytest

from app.web.charge_points import get_charge_point_service
from app.web.charge_points.models import ChargePoint

service = get_charge_point_service()


@pytest.mark.asyncio
async def test_establish_many_connections_from_charge_points_to_the_worker(
        session,
        charge_points,
        connect_to_worker,
        TEST_MAX_CHARGE_POINTS_COUNT,
        NEW_CONNECTION_AWAITING_DELAY
):
    connections = []
    try:
        for charge_point in charge_points:  # type: ChargePoint
            connection = await connect_to_worker(charge_point.id)
            connections.append(connection)
            await asyncio.sleep(NEW_CONNECTION_AWAITING_DELAY)  # wait for messages to be processed by the broker
            charge_point = await service.get_charge_point(charge_point.id, session)
            assert charge_point.connection.is_active
            assert charge_point.connection.status is None
    finally:
        await asyncio.gather(*[connection.close() for connection in connections])


@pytest.mark.asyncio
async def test_interrupt_many_connections_from_charge_points_to_the_worker(
        session,
        charge_points,
        connect_to_worker,
        TEST_MAX_CHARGE_POINTS_COUNT,
        NEW_CONNECTION_AWAITING_DELAY,
        INTERRUPTED_CONNECTION_AWAITING_DELAY
):
    for charge_point in charge_points:  # type: ChargePoint
        connection = await connect_to_worker(charge_point.id)
        try:
            await asyncio.sleep(
                INTERRUPTED_CONNECTION_AWAITING_DELAY)  # wait for messages to be processed by the broker
        finally:
            await connection.close()
            await asyncio.sleep(INTERRUPTED_CONNECTION_AWAITING_DELAY)
            charge_point = await service.get_charge_point(charge_point.id, session)
            assert not charge_point.connection.is_active
            assert charge_point.connection.status is None
