from __future__ import annotations

from uuid import uuid4

import arrow
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


def init_db(url):
    engine = create_async_engine(url)
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


def generate_default_id():
    return str(uuid4())


class Model(Base):
    __abstract__ = True

    id = Column(String(36), primary_key=True, index=True, default=generate_default_id, unique=True)
    created_at = Column(DateTime, default=lambda: arrow.utcnow().datetime.replace(tzinfo=None))
    updated_at = Column(DateTime, onupdate=lambda: arrow.utcnow().datetime.replace(tzinfo=None), nullable=True)
    is_active = Column(Boolean, default=True)
