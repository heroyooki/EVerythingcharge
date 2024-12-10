from pydantic import BaseModel, ConfigDict


class UserView(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str

    model_config = ConfigDict(from_attributes=True)


class CreateUserPayloadView(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str


class LoginPayloadView(BaseModel):
    email: str
    password: str
