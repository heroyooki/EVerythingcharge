from pydantic import BaseModel


class CreateUserView(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str


class LoginView(BaseModel):
    email: str
    password: str
