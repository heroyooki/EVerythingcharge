from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from core.models import get_contextual_session


class DBSessionMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        async with get_contextual_session() as session:
            request.scope["session"] = session
            response = await call_next(request)
            return response
