from __future__ import annotations

import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from propan import apply_types
from propan.annotations import ContextRepo
from sqlalchemy.exc import IntegrityError
from starlette.middleware.exceptions import ExceptionMiddleware

from api.connections import init_global_scope
from api.repositories.web import CookiesRepo
from api.web.auth.backends.jwt import JWTAuthenticationBackend
from api.web.auth.middlewares.jwt import JWTAuthenticationMiddleware
from api.web.charge_points.controllers import router as charge_points_router
from api.web.exceptions.handlers import unique_violation_exception_handler, common_exceptions_handler
from api.web.networks.controllers import private_router as networks_private_router
from api.web.users.controllers import (
    public_router as users_public_router,
    private_router as users_private_router
)
from core.annotations import TasksRepo
from core.broker import broker
from core.middlewares import DBSessionMiddleware
from core.settings import ALLOWED_ORIGIN

app = FastAPI(
    exception_handlers={
        IntegrityError: unique_violation_exception_handler,
        Exception: common_exceptions_handler
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    JWTAuthenticationMiddleware,
    backend=JWTAuthenticationBackend(CookiesRepo())
)
app.add_middleware(DBSessionMiddleware)
app.add_middleware(ExceptionMiddleware, handlers=app.exception_handlers)

app.include_router(networks_private_router)
app.include_router(users_private_router)
app.include_router(users_public_router)
app.include_router(charge_points_router)


@app.on_event("startup")
@apply_types
async def startup(tasks_repo: TasksRepo, context: ContextRepo):
    task = asyncio.create_task(broker.start())
    # Save a reference to the result of this function, to avoid a task disappearing mid-execution.
    # The event loop only keeps weak references to tasks.
    tasks_repo.add(task)
    await init_global_scope(context)
