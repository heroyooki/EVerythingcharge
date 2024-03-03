import json
from typing import Annotated, Any, Dict

from propan import Depends
from propan import RabbitBroker
from propan.brokers.rabbit import (
    RabbitExchange,
    ExchangeType
)

from core import settings
from core.settings import (
    MESSAGES_BROKER_URL,
    EVENTS_EXCHANGE_NAME,
    TASKS_EXCHANGE_NAME
)

background_tasks = set()
broker = RabbitBroker(MESSAGES_BROKER_URL)


async def tasks_repo():
    return background_tasks


async def get_settings():
    return settings


TasksRepo = Annotated[set, Depends(tasks_repo)]
JSONLoader = Annotated[Dict, Depends(lambda body: json.loads(body))]
Settings = Annotated[Any, Depends(get_settings)]

events_exchange = RabbitExchange(
    EVENTS_EXCHANGE_NAME,
    auto_delete=True
)

tasks_exchange = RabbitExchange(
    TASKS_EXCHANGE_NAME,
    auto_delete=True,
    type=ExchangeType.FANOUT
)


async def get_exchange(name: str):
    return {
        EVENTS_EXCHANGE_NAME: events_exchange,
        TASKS_EXCHANGE_NAME: tasks_exchange
    }[name]


EventsExchange = Annotated[RabbitExchange, Depends(lambda: get_exchange(EVENTS_EXCHANGE_NAME))]
TasksExchange = Annotated[RabbitExchange, Depends(get_exchange(TASKS_EXCHANGE_NAME))]
