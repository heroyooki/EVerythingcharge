from typing import Dict, Union

from ocpp.v201.enums import Action
from pydantic import BaseModel


class StorePayloadView(BaseModel):
    charge_point_id: str
    call_type: int
    unique_id: str
    payload: Dict
    timestamp: str
    action: Union[Action, None] = None


class LookUpByUniqueIdView(BaseModel):
    unique_id: str
