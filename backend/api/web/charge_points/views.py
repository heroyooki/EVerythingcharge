from datetime import datetime
from typing import Union, Optional, List

from ocpp.v16.enums import ChargePointStatus, ChargePointErrorCode
from ocpp.v201.enums import ConnectorStatusType, StatusInfoReasonType
from pydantic import BaseModel, field_validator, Field

from api.web.views import PaginationView


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


class UpdateChargePointPayloadView(BaseModel):
    model: Union[str, None] = None
    vendor: Union[str, None] = None
    status: Union[ChargePointStatus, ConnectorStatusType, None] = None
    error_code: Union[ChargePointErrorCode, StatusInfoReasonType] = None
    evse_id: Union[int, None] = None


class SimpleChargePoint(BaseModel):
    id: str
    ocpp_version: str
    status: Union[ChargePointStatus, ConnectorStatusType]
    location: str | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class SimpleConnectorView(BaseModel):
    id: int
    status: Union[ChargePointStatus, ConnectorStatusType]
    error_code: Union[ChargePointErrorCode, None] = None

    class Config:
        from_attributes = True


class ChargePointView(BaseModel):
    id: str
    ocpp_version: str
    location: str | None = None
    description: str | None = None
    status: Union[ChargePointStatus, ConnectorStatusType]
    model: str | None = None
    vendor: str | None = None
    updated_at: datetime | None = None
    connectors: List[SimpleConnectorView] = []

    class Config:
        from_attributes = True


class PaginatedChargePointsView(BaseModel):
    items: List[SimpleChargePoint]
    pagination: PaginationView
