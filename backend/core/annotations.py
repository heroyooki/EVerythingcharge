from typing import Annotated, Any

from propan import apply_types, Depends
from propan.brokers.rabbit import RabbitExchange


def get_settings():
    from core import settings

    return settings


Settings = Annotated[Any, Depends(get_settings)]


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
async def get_logger():
    from loguru import logger
    return logger


Logger = Annotated[Any, Depends(get_logger)]
TasksRepo = Annotated[set, Depends(get_tasks_repository)]
EventsExchange = Annotated[RabbitExchange, Depends(get_events_exchange)]
TasksExchange = Annotated[RabbitExchange, Depends(get_tasks_exchange)]
