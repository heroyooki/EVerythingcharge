from loguru import logger
from ocpp.routing import on
from ocpp.v201 import call_result
from ocpp.v201.enums import Action, DataTransferStatusType
from propan import apply_types


class DataTransferScenario:

    @apply_types
    @on(Action.DataTransfer)
    async def on_data_transfer(self_, vendor_id: str):
        logger.info(
            f"Accepted '{Action.DataTransfer}' "
            f"(vendor_id={vendor_id})"
        )
        return call_result.DataTransferPayload(status=DataTransferStatusType.rejected)
