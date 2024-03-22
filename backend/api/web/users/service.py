from typing import Dict, Annotated, Union

from fastapi import Depends
from passlib.context import CryptContext
from propan import apply_types
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from api.web.users.models import User
from api.web.users.views import LoginPayloadView
from core.models import get_session

_password_context: CryptContext | None = None


def get_password_context() -> CryptContext:
    global _password_context
    if not _password_context:
        _password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return _password_context


@apply_types
async def create_user(
        data: Dict,
        session: AsyncSession = Depends(get_session),
) -> User:
    data["password"] = get_password_context().hash(data["password"])
    user = User(**data)
    session.add(user)
    return user


async def get_user(
        email: "Email",
        session: AsyncSession = Depends(get_session)
) -> User | None:
    result = await session.execute(
        select(User) \
            .where(or_(User.id == email, User.email == email))
    )
    user = result.scalars().first()
    return user


def get_email(data: Union[LoginPayloadView, str]):
    return getattr(data, "email", data)


def get_password(data: Union[LoginPayloadView, str]):
    return getattr(data, "password", data)


Email = Annotated[Union[LoginPayloadView, str], Depends(get_email)]
Password = Annotated[Union[LoginPayloadView, str], Depends(get_password)]
AnnotatedUser = Annotated[User, Depends(get_user)]
PasswdContext = Annotated[CryptContext, Depends(get_password_context)]
