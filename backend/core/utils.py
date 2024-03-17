from datetime import datetime
from typing import Dict, Any

import arrow
from propan import apply_types, Depends, Context


def get_settings():
    from core import settings

    return settings


def get_utc() -> datetime:
    return arrow.utcnow().datetime


@apply_types
def get_formatted_utc(
        utc: datetime = Depends(get_utc),
        settings: Any = Depends(get_settings)
) -> str:
    return utc.strftime(settings.UTC_DATETIME_FORMAT)


@apply_types
async def get_default_amqp_headers(
        charge_point_id: str = Context(),
        settings: Any = Depends(get_settings)
):
    return {
        settings.CHARGE_POINT_ID_HEADER_NAME: charge_point_id
    }


@apply_types
async def get_tasks_repository(settings: Any = Depends(get_settings)):
    return settings.background_tasks


@apply_types
async def get_events_exchange(settings: Any = Depends(get_settings)):
    return settings.events_exchange


@apply_types
async def get_tasks_exchange(settings: Any = Depends(get_settings)):
    return settings.tasks_exchange


@apply_types
async def get_connections_exchange(settings: Any = Depends(get_settings)):
    return settings.connections_exchange


async def get_id_from_amqp_headers(
        settings: Any = Depends(get_settings),
        headers: Dict = Context("message.headers"),
) -> str:
    result = headers[settings.CHARGE_POINT_ID_HEADER_NAME]
    return result
