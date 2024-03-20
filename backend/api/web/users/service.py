from typing import Dict

from passlib.context import CryptContext
from propan import apply_types, Depends, Context

from api.web.users.models import User

_password_context = None


def get_password_context() -> CryptContext:
    global _password_context
    if not _password_context:
        _password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return _password_context


@apply_types
async def create_user(
        data: Dict,
        session=Context(),
        passwd_context: CryptContext = Depends(get_password_context),
) -> User:
    data["password"] = passwd_context.hash(data["password"])
    user = User(**data)
    session.add(user)
    return user
