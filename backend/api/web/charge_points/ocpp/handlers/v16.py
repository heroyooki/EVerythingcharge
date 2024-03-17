from ocpp.v16 import ChargePoint as ChargePoint16

from api.web.charge_points.ocpp.handlers.base import OCPPHandler
from api.web.charge_points.ocpp.scenarios.v16.boot_notification import BootNotificationScenario


class OCPP16Handler(
    OCPPHandler,
    ChargePoint16,
    BootNotificationScenario
):
    pass
