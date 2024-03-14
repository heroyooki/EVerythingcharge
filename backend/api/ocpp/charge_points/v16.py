from api.ocpp.charge_points import ChargePoint as cp
from api.rest.charge_points.scenarios.v16.boot_notification import BootNotificationScenario


class ChargePoint(
    cp,
    BootNotificationScenario
):
    _ocpp_version = "1.6"
