from ocpp.v201 import ChargePoint as ChargePoint201

from api.web.charge_points.handlers.base import OCPPHandler


class OCPP201Handler(
    OCPPHandler,
    ChargePoint201
):
    pass
