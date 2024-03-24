import arrow
from jose import jwt
from propan import Depends, apply_types
from starlette.authentication import AuthenticationBackend as BaseAuthenticationBackend

from api.repositories.web import WebRepository
from api.web.auth.views import AuthToken
from core.utils import get_settings


class AuthenticationBackend(BaseAuthenticationBackend):

    def __init__(self, repository: WebRepository):
        self.repository = repository

    @apply_types
    async def read_token(self_, identity: str, settings=Depends(get_settings)) -> AuthToken:
        token = jwt.decode(identity, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return AuthToken(**token)

    @apply_types
    async def create_token(self_, user_id: str, settings=Depends(get_settings)) -> str:
        token = AuthToken(
            user_id=str(user_id),
            expires=arrow.utcnow().shift(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) \
                .datetime.strftime(settings.UTC_DATETIME_FORMAT)
        )

        return jwt.encode(token.dict(), settings.SECRET_KEY, algorithm=settings.ALGORITHM)
