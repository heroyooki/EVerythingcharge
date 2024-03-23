from __future__ import annotations

from propan import RabbitBroker
from propan.brokers.rabbit import RabbitExchange, ExchangeType

from core.settings import (
    MESSAGES_BROKER_URL,
    EVENTS_EXCHANGE_NAME,
    TASKS_EXCHANGE_NAME,
    CONNECTIONS_EXCHANGE_NAME
)

broker = RabbitBroker(MESSAGES_BROKER_URL)
events_exchange = RabbitExchange(
    EVENTS_EXCHANGE_NAME,
    auto_delete=True
)
tasks_exchange = RabbitExchange(
    TASKS_EXCHANGE_NAME,
    auto_delete=True,
    type=ExchangeType.FANOUT
)
connections_exchange = RabbitExchange(
    CONNECTIONS_EXCHANGE_NAME,
    auto_delete=True,
    type=ExchangeType.TOPIC
)
