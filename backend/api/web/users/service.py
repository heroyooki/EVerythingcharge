from typing import Annotated, Union

from fastapi import Depends
from passlib.context import CryptContext
from propan import apply_types, Context
from sqlalchemy import select, or_

from api.web.users.models import User
from api.web.users.views import LoginPayloadView, CreateUserPayloadView

_password_context: CryptContext | None = None


def get_email(data: Union[LoginPayloadView, str]):
    return getattr(data, "email", data)


def get_password(data: Union[LoginPayloadView, str]):
    return getattr(data, "password", data)


Email = Annotated[Union[LoginPayloadView, str], Depends(get_email)]


def get_password_context() -> CryptContext:
    global _password_context
    if not _password_context:
        _password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return _password_context


@apply_types
async def create_user(
        data: CreateUserPayloadView,
        session=Context(),
):
    data.password = get_password_context().hash(data.password)
    user = User(**data.dict())
    session.add(user)
    await session.flush()
    return user


@apply_types
async def get_user_by_email(
        email: Email,
        session=Context()
) -> User | None:
    result = await session.execute(
        select(User) \
            .where(or_(User.email == email))
    )
    user = result.scalars().first()
    return user


@apply_types
async def get_user_by_id(
        user_id: str,
        session=Context()
) -> User | None:
    result = await session.execute(
        select(User) \
            .where(or_(User.id == user_id))
    )
    user = result.scalars().first()
    return user


Password = Annotated[Union[LoginPayloadView, str], Depends(get_password)]
AnnotatedUser = Annotated[User, Depends(get_user_by_email)]
PasswdContext = Annotated[CryptContext, Depends(get_password_context)]
