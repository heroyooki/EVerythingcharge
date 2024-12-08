from __future__ import annotations

from contextlib import asynccontextmanager

from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.ext.asyncio import AsyncSession

from core import settings
from core.models import init_db

mongo_client = AsyncIOMotorClient(settings.MONGODB_URI)
db = mongo_client[settings.MONGODB_NAME]


async def ensure_indexes():
    collection = db[settings.MONGODB_PAYLOADS_COLLECTION_NAME]
    await collection.create_index([("unique_id", 1)], unique=False)
    await collection.create_index([("charge_point_id", 1)], unique=False)


@asynccontextmanager
async def get_mongo_collection(collection_name: str):
    collection = db[collection_name]
    yield collection


asession = init_db(settings.DATABASE_ASYNC_URL)


@asynccontextmanager
async def get_contextual_session() -> AsyncSession:
    async with asession() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_session() -> AsyncSession:
    async with asession() as session:
        try:
            yield session
        finally:
            await session.close()
