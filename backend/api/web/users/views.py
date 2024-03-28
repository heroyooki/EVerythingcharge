from typing import List, Any

from pydantic import BaseModel


class UserView(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    networks: List[Any] = []


class CreateUserPayloadView(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str


class LoginPayloadView(BaseModel):
    email: str
    password: str
