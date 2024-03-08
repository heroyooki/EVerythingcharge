from fast_depends.library import CustomField
from propan import Context

from api.charge_point import OCPP16ChargePoint
from core.annotations import Settings


class ChargePoint(CustomField):
    def use(self, /, **kwargs):
        kwargs = super().use(**kwargs)
        assert kwargs.get("charge_point_id"), "Expect 'charge_point_id' as an argument in the signature."
        kwargs[self.param_name] = OCPP16ChargePoint(charge_point_id=kwargs["charge_point_id"])
        return kwargs


async def get_id_from_headers(
        settings: Settings,
        headers=Context("message.headers")
):
    return headers[settings.CHARGE_POINT_ID_HEADER_NAME]
