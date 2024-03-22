from http import HTTPStatus

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from api.web.auth.backends.jwt import JWTAuthenticationBackend
from core import settings


class JWTAuthenticationMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app: ASGIApp,
            backend: JWTAuthenticationBackend,
    ):
        super().__init__(app)
        self.backend = backend

    async def dispatch(self, request: Request, call_next):
        user = await self.backend.authenticate(request)
        request.scope["user"] = user

        response = await call_next(request)
        if HTTPStatus(response.status_code) is HTTPStatus.UNAUTHORIZED:
            await self.backend.repository.unset_for_next(response)
            return response

        # User id is being stored in 'X-Authenticated' header after successful login
        user_id = response.headers.get("X-Authenticated") or getattr(user, "id", None)
        if user_id:
            token = await self.backend.create_token(user_id, settings)
            await self.backend.repository.set_for_next(token, response)
        # Requests to the public endpoints are assumed.
        return response
