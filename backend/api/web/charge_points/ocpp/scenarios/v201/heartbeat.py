from loguru import logger
from ocpp.routing import on
from ocpp.v201 import call_result
from ocpp.v201.enums import Action
from propan import Depends
from propan import apply_types

from core.utils import get_formatted_utc


class HeartbeatScenario:

    @apply_types
    @on(Action.Heartbeat)
    async def on_heartbeat(
            self_,
            utc_datetime: str = Depends(get_formatted_utc)
    ):
        logger.info(
            f"Accepted '{Action.Heartbeat}' "
            f"(charge_point_id={self_.id})"
        )
        return call_result.HeartbeatPayload(current_time=utc_datetime)
