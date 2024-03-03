import json
from typing import Annotated, Any, Dict, List, Union

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

TasksRepo = Annotated[set, Depends(lambda: background_tasks)]
PayloadJsonLoader = Annotated[
    Union[Dict, List], Depends(lambda payload: json.loads(payload) if isinstance(payload, str) else payload)]
PayloadJsonDumper = Annotated[
    str, Depends(lambda payload: json.dumps(payload) if isinstance(payload, Dict) else payload)]
Settings = Annotated[Any, Depends(lambda: settings)]

events_exchange = RabbitExchange(
    EVENTS_EXCHANGE_NAME,
    auto_delete=True
)

tasks_exchange = RabbitExchange(
    TASKS_EXCHANGE_NAME,
    auto_delete=True,
    type=ExchangeType.FANOUT
)

EventsExchange = Annotated[RabbitExchange, Depends(lambda: events_exchange)]
TasksExchange = Annotated[RabbitExchange, Depends(lambda: tasks_exchange)]
