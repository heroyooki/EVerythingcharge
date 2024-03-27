from ocpp.v201 import ChargePoint as ChargePoint201

from api.web.charge_points.ocpp.handlers.base import OCPPHandler
from api.web.charge_points.ocpp.scenarios.v201.boot_notification import BootNotificationScenario
from api.web.charge_points.ocpp.scenarios.v201.status_notification import StatusNotificationScenario


class OCPP201Handler(
    OCPPHandler,
    ChargePoint201,

    BootNotificationScenario,
    StatusNotificationScenario
):
    pass
