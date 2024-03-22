from pydantic import BaseModel


class CreateUserPayloadView(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str


class LoginPayloadView(BaseModel):
    email: str
    password: str
