from pydantic import BaseModel


class CreateAccountPayloadView(BaseModel):
    name: str
