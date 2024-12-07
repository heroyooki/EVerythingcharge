from typing import Union, Dict

from ocpp.v201.enums import BootReasonType
from pydantic import BaseModel


class ConnectionView(BaseModel):
    status: Union[str, None] = None
    reason: Union[BootReasonType, None] = None
    custom_data: Dict = dict()
