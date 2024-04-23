from loguru import logger
from ocpp.routing import on
from ocpp.v16 import call_result
from ocpp.v16.enums import Action, DataTransferStatus
from propan import apply_types


class DataTransferScenario:

    @apply_types
    @on(Action.DataTransfer)
    async def on_data_transfer(self_, vendor_id: str):
        logger.info(
            f"Accepted '{Action.DataTransfer}' "
            f"(vendor_id={vendor_id})"
        )

        return call_result.DataTransferPayload(status=DataTransferStatus.rejected)
