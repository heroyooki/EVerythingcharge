from typing import Any

import arrow
from fastapi import Depends
from jose import jwt
from starlette.authentication import AuthenticationBackend as BaseAuthenticationBackend

from api.web.auth.repositories import WebRepository
from api.web.auth.views import AuthToken
from core.utils import get_settings


class AuthenticationBackend(BaseAuthenticationBackend):

    def __init__(self, repository: WebRepository):
        self.repository = repository

    async def read_token(
            self,
            identity: str,
            settings: Any = Depends(get_settings),
            lib: Any = Depends(lambda: jwt)
    ) -> AuthToken:
        token = lib.decode(identity, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return AuthToken(**token)

    async def create_token(
            self,
            user_id: str,
            settings: Any = Depends(get_settings),
            lib: Any = Depends(lambda: jwt)
    ) -> str:
        token = AuthToken(
            user_id=str(user_id),
            expires=arrow.utcnow().shift(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) \
                .datetime.strftime(settings.UTC_DATETIME_FORMAT)
        )

        return lib.encode(token.dict(), settings.SECRET_KEY, algorithm=settings.ALGORITHM)
