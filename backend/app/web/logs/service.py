import json
from typing import Union, List

from ocpp.messages import MessageType
from propan import apply_types, Depends

from app.web.logs.views import StorePayloadView, LookUpByUniqueIdView
from core.dependencies import get_settings, get_formatted_utc
from core.repositories import get_mongo_collection


@apply_types
async def store_payload(
        charge_point_id: str,
        data: Union[str, List],
        settings=Depends(get_settings),
        utc_datetime=Depends(get_formatted_utc)
):
    try:
        data: List = json.loads(data)
    except json.JSONDecodeError:
        pass
    call_type = data[0]
    action = None
    if call_type is MessageType.Call:
        _, unique_id, action, payload = data
    else:
        _, unique_id, payload = data
    async with get_mongo_collection(settings.MONGODB_PAYLOADS_COLLECTION_NAME) as collection:
        view = StorePayloadView(
            charge_point_id=charge_point_id,
            call_type=call_type,
            unique_id=unique_id,
            payload=payload,
            timestamp=utc_datetime,
            action=action
        )
        await collection.insert_one(view.model_dump())


@apply_types
async def find_payloads_by_id(unique_id: str, settings=Depends(get_settings)):
    """
    Unique id is an id of the message, not collections row.
    """
    async with get_mongo_collection(settings.MONGODB_PAYLOADS_COLLECTION_NAME) as collection:
        view = LookUpByUniqueIdView(unique_id=unique_id)
        cursor = collection.find(view.model_dump(), {"_id": 0})
        documents = await cursor.to_list(length=None)
        return documents
