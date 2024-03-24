from datetime import datetime
from typing import Dict, Any

import arrow
from propan import Depends, Context

from core import settings
from core.broker import tasks_exchange, events_exchange, connections_exchange
from core.settings import background_tasks


def get_settings():
    return settings


def get_utc() -> datetime:
    return arrow.utcnow().datetime


def get_formatted_utc(
        utc: datetime = Depends(get_utc),
        settings: Any = Depends(get_settings)
) -> str:
    return utc.strftime(settings.UTC_DATETIME_FORMAT)


async def get_default_amqp_headers(
        charge_point_id: str = Context(),
        settings: Any = Depends(get_settings)
):
    return {
        settings.CHARGE_POINT_ID_HEADER_NAME: charge_point_id
    }


async def get_tasks_repository():
    return background_tasks


async def get_events_exchange():
    return events_exchange


async def get_tasks_exchange():
    return tasks_exchange


async def get_connections_exchange():
    return connections_exchange


async def get_id_from_amqp_headers(
        settings: Any = Depends(get_settings),
        headers: Dict = Context("message.headers"),
) -> str:
    result = headers[settings.CHARGE_POINT_ID_HEADER_NAME]
    return result
