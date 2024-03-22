from __future__ import annotations

from typing import Annotated, Dict

from propan import Depends
from propan.brokers.rabbit import RabbitExchange

import core.utils as utils

TasksRepo = Annotated[set, Depends(utils.get_tasks_repository)]
AMQPHeaders = Annotated[Dict, Depends(utils.get_default_amqp_headers)]
EventsExchange = Annotated[RabbitExchange, Depends(utils.get_events_exchange)]
TasksExchange = Annotated[RabbitExchange, Depends(utils.get_tasks_exchange)]
ConnectionsExchange = Annotated[RabbitExchange, Depends(utils.get_connections_exchange)]
