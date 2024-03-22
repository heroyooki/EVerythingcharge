from typing import Union, Any

import arrow
from fastapi import Depends, Request
from starlette.authentication import UnauthenticatedUser

from api.web.auth.backends.base import AuthenticationBackend
from api.web.users import get_users_service
from api.web.users.models import User
from core.utils import get_settings


class JWTAuthenticationBackend(AuthenticationBackend):

    async def authenticate(
            self,
            request: Request,
            settings: Any = Depends(get_settings),
            anonymous_user: UnauthenticatedUser = Depends(lambda: UnauthenticatedUser()),
            service: Any = Depends(get_users_service),
    ) -> Union[User, UnauthenticatedUser]:
        identity = await self.repository.extract_token(request)
        try:
            token = await self.read_token(identity, settings)
        except Exception:
            return anonymous_user

        user = await service.get_user(token.user_id)
        if arrow.get(token.expires) < arrow.utcnow() or not user:
            return anonymous_user

        return user
