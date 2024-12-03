from __future__ import annotations

from contextlib import asynccontextmanager
from uuid import uuid4

import arrow
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from core import settings


def init_db(url):
    engine = create_async_engine(url)
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


asession = init_db(settings.DATABASE_ASYNC_URL)
Base = declarative_base()


async def get_session() -> AsyncSession:
    async with asession() as session:
        try:
            yield session
        finally:
            await session.close()


@asynccontextmanager
async def get_contextual_session() -> AsyncSession:
    async with asession() as session:
        try:
            yield session
        finally:
            await session.close()


def generate_default_id():
    # ocpp requires max 20 characters for some id values
    return uuid4().hex[:20]


class Model(Base):
    __abstract__ = True

    id = Column(String(20), primary_key=True, index=True, default=generate_default_id, unique=True)
    created_at = Column(DateTime, default=lambda: arrow.utcnow().datetime.replace(tzinfo=None))
    updated_at = Column(DateTime, onupdate=lambda: arrow.utcnow().datetime.replace(tzinfo=None), nullable=True)
    is_active = Column(Boolean, default=True)
