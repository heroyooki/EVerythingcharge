import asyncio
import json

import pytest
from ocpp.v201.enums import ConnectorStatusType

from app.web.charge_points import get_charge_point_service
from app.web.charge_points.models import ChargePoint
from app.web.logs import get_logs_service

service = get_charge_point_service()
logs_service = get_logs_service()


@pytest.mark.asyncio
async def test_accept_many_status_notifications_over_charge_point(
        session,
        charge_points,
        connect_to_worker,
        TEST_MAX_CHARGE_POINTS_COUNT,
        NEW_CONNECTION_AWAITING_DELAY,
        StatusNotificationMessageWithAvailableStatus
):
    connections = []
    try:
        for charge_point in charge_points:  # type: ChargePoint
            connection = await connect_to_worker(charge_point.id)
            await asyncio.sleep(NEW_CONNECTION_AWAITING_DELAY)
            message = StatusNotificationMessageWithAvailableStatus(evse_id=0, connector_id=0)
            _, call_unique_id, _, call_payload = message
            connections.append((call_unique_id, call_payload, charge_point, connection))
            await connection.send(json.dumps(message))
        for item in connections:
            call_unique_id, call_payload, charge_point, connection = item
            payload = await connection.recv()
            data = json.loads(payload)
            charge_point = await service.get_charge_point(charge_point.id, session)
            assert isinstance(data, list)
            assert ConnectorStatusType(charge_point.connection.status) is ConnectorStatusType.available
            logs = await logs_service.find_payloads_by_id(call_unique_id)
            assert len(logs) == 2  # 2 messages: call and call_result
    finally:
        await asyncio.gather(*[connection[-1].close() for connection in connections])
