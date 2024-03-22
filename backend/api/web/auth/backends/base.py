from typing import Any

import arrow
from jose import jwt
from starlette.authentication import AuthenticationBackend as BaseAuthenticationBackend

from api.web.auth.repositories import WebRepository
from api.web.auth.views import AuthToken


class AuthenticationBackend(BaseAuthenticationBackend):

    def __init__(self, repository: WebRepository):
        self.repository = repository

    async def read_token(
            self,
            identity: str,
            settings: Any,
    ) -> AuthToken:
        token = jwt.decode(identity, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return AuthToken(**token)

    async def create_token(
            self,
            user_id: str,
            settings: Any
    ) -> str:
        token = AuthToken(
            user_id=str(user_id),
            expires=arrow.utcnow().shift(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) \
                .datetime.strftime(settings.UTC_DATETIME_FORMAT)
        )

        return jwt.encode(token.dict(), settings.SECRET_KEY, algorithm=settings.ALGORITHM)
