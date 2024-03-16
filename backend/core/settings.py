from __future__ import annotations

import os

from loguru import logger
from propan.brokers.rabbit import RabbitExchange, RabbitBroker, ExchangeType

DEBUG = os.environ.get("DEBUG") == "1"
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.curdir)))

TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

DB_NAME = os.environ["DB_NAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_PORT = int(os.environ["DB_PORT"])
DB_USER = os.environ["DB_USER"]
DB_HOST = os.environ["DB_HOST"]

WS_SERVER_PORT = int(os.environ["WS_SERVER_PORT"])

DATABASE_ASYNC_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
DATABASE_SYNC_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

logger.add(
    "everythingcharge.log",
    enqueue=True,
    backtrace=True,
    diagnose=DEBUG,
    format="{time} - {level} - {message}",
    rotation="500 MB",
    level="INFO"
)

DATETIME_FORMAT = "YYYY-MM-DD HH:mm:ss"
UTC_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

RABBITMQ_PORT = os.environ["RABBITMQ_PORT"]
RABBITMQ_UI_PORT = os.environ["RABBITMQ_UI_PORT"]
RABBITMQ_USER = os.environ["RABBITMQ_USER"]
RABBITMQ_PASS = os.environ["RABBITMQ_PASS"]
RABBITMQ_HOST = os.environ["RABBITMQ_HOST"]

MESSAGES_BROKER_URL = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/"

EVENTS_EXCHANGE_NAME = os.environ.get("EVENTS_EXCHANGE_NAME", "events")
EVENTS_QUEUE_NAME = os.environ.get("EVENTS_QUEUE_NAME", "events")

NEW_CONNECTION_QUEUE_NAME = os.environ.get("NEW_CONNECTION_QUEUE_NAME", "new_connections")
LOST_CONNECTION_QUEUE_NAME = os.environ.get("LOST_CONNECTION_QUEUE_NAME", "lost_connections")

TASKS_EXCHANGE_NAME = os.environ.get("TASKS_EXCHANGE_NAME", "tasks")

CONNECTIONS_EXCHANGE_NAME = os.environ.get("CONNECTIONS_EXCHANGE_NAME", "connections")
FORCE_CLOSE_CONNECTION_QUEUE_NAME = os.environ.get("FORCE_CLOSE_CONNECTION_QUEUE_NAME", "force_close")

MAX_MESSAGE_PRIORITY = 10
REGULAR_MESSAGE_PRIORITY = 5
LOW_MESSAGE_PRIORITY = 1

HTTP_SERVER_PORT = int(os.environ["HTTP_SERVER_PORT"])

# Response from the charging station
RESPONSE_TIMEOUT = int(os.environ.get("RESPONSE_TIMEOUT", 30))

CHARGE_POINT_ID_HEADER_NAME = "Charge-Point-Id"
background_tasks = set()
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

HEARTBEAT_INTERVAL = int(os.environ.get("HEARTBEAT_INTERVAL", 60))
