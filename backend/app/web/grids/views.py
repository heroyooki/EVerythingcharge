from typing import Union

from pydantic import BaseModel


class CreateGridPayloadView(BaseModel):
    account_id: str
    name: str
    capacity: Union[int, None] = None
    unit: str
    supplier: str
