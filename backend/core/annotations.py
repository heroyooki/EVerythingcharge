from __future__ import annotations

from typing import Annotated, Dict

from propan import Depends
from propan.brokers.rabbit import RabbitExchange

import core.dependencies as dependencies

TasksRepo = Annotated[set, Depends(dependencies.get_tasks_repository)]
AMQPHeaders = Annotated[Dict, Depends(dependencies.get_default_amqp_headers)]
EventsExchange = Annotated[RabbitExchange, Depends(dependencies.get_events_exchange)]
TasksExchange = Annotated[RabbitExchange, Depends(dependencies.get_tasks_exchange)]
ConnectionsExchange = Annotated[RabbitExchange, Depends(dependencies.get_connections_exchange)]
