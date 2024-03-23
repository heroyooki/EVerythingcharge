from typing import Union, Any

import arrow
from fastapi import Request
from starlette.authentication import UnauthenticatedUser

from api.web.auth.backends.base import AuthenticationBackend
from api.web.users import service
from api.web.users.models import User


class JWTAuthenticationBackend(AuthenticationBackend):

    async def authenticate(
            self,
            request: Request,
            anonymous_user: Any = UnauthenticatedUser()
    ) -> Union[User, UnauthenticatedUser]:
        identity = await self.repository.extract_token(request)
        try:
            token = await self.read_token(identity)
        except Exception:
            return anonymous_user

        user = await service.get_user_by_id(user_id=token.user_id)
        if arrow.get(token.expires) < arrow.utcnow() or not user:
            return anonymous_user

        return user
