from typing import Union, Dict

from ocpp.v201.enums import BootReasonType, ConnectorStatusType
from pydantic import BaseModel


class ConnectionView(BaseModel):
    status: Union[ConnectorStatusType, None] = None
    reason: Union[BootReasonType, None] = None
    custom_data: Dict = dict()
    is_active: bool = None
