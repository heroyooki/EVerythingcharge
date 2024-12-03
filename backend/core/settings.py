from __future__ import annotations

import os
import sys

from loguru import logger

DEBUG = os.environ.get("DEBUG") == "1"
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname((__file__))))

DB_NAME = os.environ["DB_NAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_PORT = int(os.environ["DB_PORT"])
DB_USER = os.environ["DB_USER"]
DB_HOST = os.environ["DB_HOST"]

WS_SERVER_PORT = int(os.environ["WS_SERVER_PORT"])

DATABASE_ASYNC_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
DATABASE_SYNC_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

format = "{time} - {level} - {file} - {message} - {extra}"
logger.add(
    sys.stdout,
    enqueue=True,
    backtrace=True,
    format=format,
    level="INFO",
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

HEARTBEAT_INTERVAL = int(os.environ.get("HEARTBEAT_INTERVAL", 60))

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])
ALLOWED_ORIGIN = os.environ["ALLOWED_ORIGIN"]

DEFAULT_USER_FIRST_NAME = os.environ["DEFAULT_USER_FIRST_NAME"]
DEFAULT_USER_LAST_NAME = os.environ["DEFAULT_USER_LAST_NAME"]
DEFAULT_USER_LOGIN = os.environ["DEFAULT_USER_LOGIN"]
DEFAULT_USER_PASSWORD = os.environ["DEFAULT_USER_PASSWORD"]
