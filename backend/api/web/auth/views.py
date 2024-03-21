from pydantic import BaseModel


class AuthToken(BaseModel):
    user_id: str
    expires: str
