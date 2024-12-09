import asyncio
import json

import arrow
import pytest
from ocpp.messages import MessageType
from ocpp.v201.enums import BootReasonType, RegistrationStatusType

from app.web.charge_points import get_charge_point_service
from app.web.charge_points.models import ChargePoint
from app.web.logs import get_logs_service

service = get_charge_point_service()
logs_service = get_logs_service()


@pytest.mark.asyncio
async def test_accept_many_boot_notifications_from_charge_points_by_the_worker(
        session,
        charge_points,
        connect_to_worker,
        TEST_MAX_CHARGE_POINTS_COUNT,
        NEW_CONNECTION_AWAITING_DELAY,
        BootNotificationMessageWithPowerUp
):
    connections = []
    try:
        for charge_point in charge_points:  # type: ChargePoint
            connection = await connect_to_worker(charge_point.id)
            await asyncio.sleep(NEW_CONNECTION_AWAITING_DELAY)
            message = BootNotificationMessageWithPowerUp()
            _, call_unique_id, _, call_payload = message
            connections.append((call_unique_id, call_payload, charge_point, connection))
            await connection.send(json.dumps(message))
        for item in connections:
            call_unique_id, call_payload, charge_point, connection = item
            payload = await connection.recv()
            data = json.loads(payload)
            charge_point = await service.get_charge_point(charge_point.id, session)
            assert isinstance(data, list)
            assert BootReasonType(charge_point.connection.reason) is BootReasonType.power_up
            message_type, call_result_unique_id, call_result_payload = data
            assert call_unique_id == call_result_unique_id
            assert message_type is MessageType.CallResult
            assert charge_point.model == call_payload["chargingStation"]["model"]
            assert charge_point.vendor_name == call_payload["chargingStation"]["vendorName"]
            assert RegistrationStatusType(call_result_payload["status"]) is RegistrationStatusType.accepted
            arrow.get(call_result_payload["currentTime"])
            assert isinstance(call_result_payload["interval"], int) and call_result_payload["interval"] > 0
            logs = await logs_service.find_payloads_by_id(call_unique_id)
            assert len(logs) == 2  # 2 messages: call and call_result
    finally:
        await asyncio.gather(*[connection[-1].close() for connection in connections])
