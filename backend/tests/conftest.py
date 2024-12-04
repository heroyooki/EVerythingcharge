from uuid import uuid4

import pytest
import pytest_asyncio
import websockets
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from api.web.charge_points import get_charge_point_service
from api.web.charge_points.views import CreateChargPointPayloadView
from core.dependencies import get_settings
from core.settings import WS_SERVER_PORT

settings = get_settings()


@pytest.fixture
def TEST_MAX_CHARGE_POINTS_COUNT():
    return 200


@pytest.fixture
def NEW_CONNECTION_AWAITING_DELAY():
    return 0.2


@pytest.fixture
def INTERRUPTED_CONNECTION_AWAITING_DELAY():
    return 0.7


@pytest.fixture
def connect_to_worker():
    async def _connect_to_worker(charge_point_id):
        uri = f"ws://everythingcharge-worker:{WS_SERVER_PORT}/%s" % charge_point_id
        return await websockets.connect(
            uri,
            subprotocols=settings.OCPP_SUBPROTOCOLS,
            extra_headers=[("Sec-WebSocket-Protocol", settings.OCPP_SUBPROTOCOLS[0])],
        )

    return _connect_to_worker


@pytest_asyncio.fixture(scope="function")
async def session():
    test_engine = create_async_engine(
        settings.DATABASE_ASYNC_URL,
        future=True,
        echo=True,
    )
    AsyncSessionLocal = sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)

    # Создаем сессию
    async with AsyncSessionLocal() as session:
        yield session
        await session.close()


@pytest.fixture
def CHARGE_POINT_DATA():
    return CreateChargPointPayloadView(
        id=uuid4().hex[:20],
        network_id=None
    )


@pytest.fixture
def CHARGE_POINTS_DATA(TEST_MAX_CHARGE_POINTS_COUNT):
    return [CreateChargPointPayloadView(
        id=uuid4().hex[:20],
        network_id=None
    ) for i in range(TEST_MAX_CHARGE_POINTS_COUNT)]


@pytest_asyncio.fixture
async def charge_points(CHARGE_POINTS_DATA, session):
    charge_points = []
    service = get_charge_point_service()

    for data in CHARGE_POINTS_DATA:
        cp = await service.create_charge_point(data, session)
        charge_points.append(cp)
    await session.commit()
    try:
        yield charge_points
    finally:
        await service.delete_charge_points([cp.id for cp in charge_points], session)
        await session.commit()


@pytest_asyncio.fixture
async def charge_point(CHARGE_POINT_DATA, session):
    service = get_charge_point_service()
    charge_point = await service.create_charge_point(CHARGE_POINT_DATA, session)
    await session.commit()
    try:
        yield charge_point
    finally:
        await service.delete_charge_points([charge_point.id], session)
        await session.commit()
