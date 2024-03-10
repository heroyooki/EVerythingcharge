from typing import Annotated, Any, Dict

from propan import apply_types, Depends, Context
from propan.brokers.rabbit import RabbitExchange


def get_settings():
    from core import settings

    return settings


Settings = Annotated[Any, Depends(get_settings)]


@apply_types
async def get_default_amqp_headers(settings: Settings, charge_point_id=Context()):
    return {
        settings.CHARGE_POINT_ID_HEADER_NAME: charge_point_id
    }


@apply_types
async def get_tasks_repository(settings: Settings):
    return settings.background_tasks


@apply_types
async def get_events_exchange(settings: Settings):
    return settings.events_exchange


@apply_types
async def get_tasks_exchange(settings: Settings):
    return settings.tasks_exchange


@apply_types
async def get_connections_exchange(settings: Settings):
    return settings.connections_exchange


@apply_types
async def get_logger():
    from loguru import logger
    return logger


async def get_id_from_headers(
        settings: Settings,
        headers=Context("message.headers")
):
    return headers[settings.CHARGE_POINT_ID_HEADER_NAME]


AMQPHeaders = Annotated[Dict, Depends(get_default_amqp_headers)]
Logger = Annotated[Any, Depends(get_logger)]
TasksRepo = Annotated[set, Depends(get_tasks_repository)]
EventsExchange = Annotated[RabbitExchange, Depends(get_events_exchange)]
TasksExchange = Annotated[RabbitExchange, Depends(get_tasks_exchange)]
ConnectionsExchange = Annotated[RabbitExchange, Depends(get_connections_exchange)]
