from fastapi import Request
from propan import apply_types
from propan.annotations import ContextRepo
from starlette.middleware.base import BaseHTTPMiddleware

from core.repositories import get_contextual_session


class DBSessionMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        @apply_types
        async def with_session_scope(context: ContextRepo):
            async with get_contextual_session() as session:
                with context.scope("session", session):
                    response = await call_next(request)
                    await session.commit()
                    return response

        return await with_session_scope()
