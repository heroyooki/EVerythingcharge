from fast_depends.library import CustomField

from api.ocpp.charge_points.v16 import ChargePoint as OCPP16ChargePoint


class ChargePoint(CustomField):
    def use(self, /, **kwargs):
        kwargs = super().use(**kwargs)
        assert kwargs.get("charge_point_id"), "Expect 'charge_point_id' as an argument in the signature."
        kwargs[self.param_name] = OCPP16ChargePoint(charge_point_id=kwargs["charge_point_id"])
        return kwargs
