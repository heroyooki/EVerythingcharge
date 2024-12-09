from uuid import uuid4

import pytest
import pytest_asyncio
import websockets
from ocpp.v201.enums import BootReasonType, Action
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.web.accounts import get_accounts_service
from app.web.accounts.views import CreateAccountPayloadView
from app.web.charge_points import get_charge_point_service
from app.web.charge_points.views import CreateChargPointPayloadView
from app.web.grids import get_grid_service
from app.web.grids.views import CreateGridPayloadView
from core.dependencies import get_settings
from core.settings import WS_SERVER_PORT

settings = get_settings()


@pytest.fixture
def BootNotificationMessageWithPowerUp():
    def return_message():
        data = [
            2,
            str(uuid4()),
            Action.BootNotification,
            {
                "reason": BootReasonType.power_up,
                "chargingStation": {
                    "model": "SingleSocketCharger",
                    "vendorName": "VendorX"
                }
            }
        ]
        return data

    return return_message


@pytest.fixture
def TEST_MAX_CHARGE_POINTS_COUNT():
    return 50


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


@pytest_asyncio.fixture
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


@pytest_asyncio.fixture
async def ACCOUNT(session):
    data = CreateAccountPayloadView(name=uuid4().hex)
    service = get_accounts_service()
    account = await service.create_account(data.model_dump(), session)
    try:
        yield account
    finally:
        await service.delete_accounts([account.id], session)
        await session.commit()


@pytest_asyncio.fixture
async def GRID(ACCOUNT, session):
    data = CreateGridPayloadView(
        account_id=ACCOUNT.id,
        name=uuid4().hex,
        capacity=10000,
        unit="Wh",
        supplier="test"
    )
    service = get_grid_service()
    grid = await service.create_grid(data.model_dump(), session)
    try:
        yield grid
    finally:
        await service.delete_grids([grid.id], session)
        await session.commit()


@pytest.fixture
def CHARGE_POINT_DATA(GRID):
    return CreateChargPointPayloadView(
        id=uuid4().hex[:20],
        grid_id=GRID.id,
    )


@pytest.fixture
def CHARGE_POINTS_DATA(TEST_MAX_CHARGE_POINTS_COUNT, GRID):
    data = []
    for i in range(TEST_MAX_CHARGE_POINTS_COUNT):
        data.append(CreateChargPointPayloadView(
            id=uuid4().hex[:20],
            grid_id=GRID.id,
        ))
    return data


@pytest_asyncio.fixture
async def charge_points(CHARGE_POINTS_DATA, session):
    charge_points = []
    service = get_charge_point_service()

    for data in CHARGE_POINTS_DATA:
        cp = await service.create_charge_point(data.model_dump(), session)
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
    charge_point = await service.create_charge_point(CHARGE_POINT_DATA.model_dump(), session)
    await session.commit()
    try:
        yield charge_point
    finally:
        await service.delete_charge_points([charge_point.id], session)
        await session.commit()
