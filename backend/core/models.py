from uuid import uuid4

import arrow
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core import settings

engine = create_async_engine(settings.DATABASE_ASYNC_URL)
asession = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


def generate_default_id():
    chunks = str(uuid4()).split("-")
    return f"{chunks[0]}{chunks[-1]}"


class Model(Base):
    __abstract__ = True

    id = Column(String(20), primary_key=True, index=True, default=generate_default_id, unique=True)
    created_at = Column(DateTime, default=lambda: arrow.utcnow().datetime.replace(tzinfo=None))
    updated_at = Column(DateTime, onupdate=lambda: arrow.utcnow().datetime.replace(tzinfo=None), nullable=True)
    is_active = Column(Boolean, default=True)
