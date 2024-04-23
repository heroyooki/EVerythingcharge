from ocpp.v16 import ChargePoint as ChargePoint16
from ocpp.v16.call import ResetPayload
from ocpp.v16.enums import ResetStatus

from api.ocpp_contrib.handlers.base import OCPPHandler
from api.ocpp_contrib.scenarios.v16.boot_notification import BootNotificationScenario
from api.ocpp_contrib.scenarios.v16.data_transfer import DataTransferScenario
from api.ocpp_contrib.scenarios.v16.heartbeat import HeartbeatScenario
from api.ocpp_contrib.scenarios.v16.status_notification import StatusNotificationScenario


class OCPP16Handler(
    OCPPHandler,
    ChargePoint16,

    BootNotificationScenario,
    StatusNotificationScenario,
    HeartbeatScenario,
    DataTransferScenario
):
    reset_payload_class = ResetPayload
    reset_status_class = ResetStatus
