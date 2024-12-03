from datetime import datetime
from typing import Union, List, Any

from ocpp.v16.enums import ChargePointStatus, ChargePointErrorCode
from ocpp.v201.enums import ConnectorStatusType, StatusInfoReasonType
from pydantic import BaseModel, field_validator, Field, ConfigDict

from api.web.views import PaginationView


class CreateChargPointPayloadView(BaseModel):
    id: str = Field(..., max_length=20)
    network_id: Union[str, None] = None


class CreateConfigurationView(BaseModel):
    key: str
    value: Any

    @field_validator("value")
    @classmethod
    def validate_value(cls, value):
        """
        Storing all values as a string
        :param value:
        :return:
        """
        return str(value)


class ConfigurationView(BaseModel):
    key: str
    value: Any

    @field_validator("value")
    @classmethod
    def validate_value(cls, value):
        """
        :param value:
        :return:
        """
        return value.lower()


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

    model_config = ConfigDict(from_attributes=True)


class SimpleConnectorView(BaseModel):
    id: int
    status: Union[ChargePointStatus, ConnectorStatusType]
    error_code: Union[ChargePointErrorCode, None] = None

    model_config = ConfigDict(from_attributes=True)


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

    model_config = ConfigDict(from_attributes=True)


class PaginatedChargePointsView(BaseModel):
    items: List[SimpleChargePoint]
    pagination: PaginationView
