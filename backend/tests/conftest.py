from uuid import uuid4

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from api.web.charge_points import get_charge_point_service
from api.web.charge_points.views import CreateChargPointPayloadView
from core.dependencies import get_settings
from core.models import Base


@pytest_asyncio.fixture(scope="function")
async def session():
    settings = get_settings()
    engine = create_async_engine(settings.TEST_DATABASE_ASYNC_URL, future=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()

    async_session = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        print("Session created:", session)
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def CHARGE_POINT_DATA():
    return CreateChargPointPayloadView(
        id=uuid4().hex[:20],
        network_id=None
    )


@pytest_asyncio.fixture
async def charge_point(CHARGE_POINT_DATA, session):
    service = get_charge_point_service()
    charge_point = await service.create_charge_point(CHARGE_POINT_DATA, session)
    await session.commit()
    return charge_point
