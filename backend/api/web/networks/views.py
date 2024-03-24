from pydantic import BaseModel, Field


class NetworkView(BaseModel):
    id: str
    name: str
    location: str


class CreateNetworkPayloadView(BaseModel):
    name: str = Field(None, min_length=2, max_length=24)
    location: str = Field(None, min_length=2, max_length=48)
