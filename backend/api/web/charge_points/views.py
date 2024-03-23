from typing import Union, Optional

from ocpp.v16.enums import ChargePointStatus
from ocpp.v201.enums import ConnectorStatusType
from pydantic import BaseModel, field_validator, Field


class SingleChargePointView(BaseModel):
    id: str
    ocpp_version: str
    description: Optional[str]
    vendor: Optional[str]
    serial_number: Optional[str]
    model: Optional[str]
    location: Optional[str]
    status: Union[ChargePointStatus, ConnectorStatusType]


class CreateChargPointPayloadView(BaseModel):
    id: str
    ocpp_version: str
    network_id: Union[str, None] = None
    description: Optional[str] = Field(None, min_length=5, max_length=124)
    vendor: Optional[str] = Field(None, min_length=3, max_length=24)
    serial_number: Optional[str] = Field(None, min_length=3, max_length=24)
    model: Optional[str] = Field(None, min_length=3, max_length=24)
    location: Optional[str] = Field(None, min_length=3, max_length=48)
    status: Union[ChargePointStatus, ConnectorStatusType, None] = None

    class Config:
        validate_assignment = True

    @field_validator("ocpp_version")
    @classmethod
    def validate_version(cls, value):
        assert value in ["1.6", "2.0.1"], "Only versions 1.6 and 2.0.1 are supported"
        return value
