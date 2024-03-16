from typing import Annotated, Any, Dict

from propan import Depends
from propan.brokers.rabbit import RabbitExchange

from core.utils import (
    get_settings,
    get_default_amqp_headers,
    get_tasks_repository,
    get_events_exchange,
    get_tasks_exchange,
    get_connections_exchange
)

Settings = Annotated[Any, Depends(get_settings)]
TasksRepo = Annotated[set, Depends(get_tasks_repository)]
AMQPHeaders = Annotated[Dict, Depends(get_default_amqp_headers)]
EventsExchange = Annotated[RabbitExchange, Depends(get_events_exchange)]
TasksExchange = Annotated[RabbitExchange, Depends(get_tasks_exchange)]
ConnectionsExchange = Annotated[RabbitExchange, Depends(get_connections_exchange)]
