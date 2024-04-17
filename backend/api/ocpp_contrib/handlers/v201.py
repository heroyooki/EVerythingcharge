from ocpp.v201 import ChargePoint as ChargePoint201
from ocpp.v201.call import ResetPayload
from ocpp.v201.enums import ResetStatusType

from api.ocpp_contrib.handlers.base import OCPPHandler
from api.ocpp_contrib.scenarios.v201.boot_notification import BootNotificationScenario
from api.ocpp_contrib.scenarios.v201.heartbeat import HeartbeatScenario
from api.ocpp_contrib.scenarios.v201.notify_event import NotifyEventScenario
from api.ocpp_contrib.scenarios.v201.status_notification import StatusNotificationScenario


class OCPP201Handler(
    OCPPHandler,
    ChargePoint201,

    BootNotificationScenario,
    StatusNotificationScenario,
    HeartbeatScenario,
    NotifyEventScenario
):
    reset_payload_class = ResetPayload
    reset_status_class = ResetStatusType
