from __future__ import annotations

import os

from loguru import logger

DEBUG = os.environ.get("DEBUG") == "1"
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.curdir)))

TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

DB_NAME = os.environ["DB_NAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_PORT = int(os.environ["DB_PORT"])
DB_USER = os.environ["DB_USER"]
DB_HOST = os.environ["DB_HOST"]

REDIS_HOST = os.environ["REDIS_HOST"]
WS_SERVER_PORT = os.environ["WS_SERVER_PORT"]

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

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])

ALLOWED_ORIGIN = os.environ["ALLOWED_ORIGIN"]

EMAIL_USE_TLS = os.environ["EMAIL_USE_TLS"] == '1'
EMAIL_HOST = os.environ["EMAIL_HOST"]
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
EMAIL_PORT = int(os.environ["EMAIL_PORT"])
EMAIL_FROM = os.environ["EMAIL_FROM"]

DAILY_HOURS_RANGE = range(6, 22)
STATIC_PATH = "/tmp"

HTTP_TIMEOUT = 10

STRIPE_PUBLIC_KEY = os.environ["STRIPE_PUBLIC_KEY"]
STRIPE_API_KEY = os.environ["STRIPE_API_KEY"]

INVITATION_LINK_EXPIRE_AFTER = int(os.environ["INVITATION_LINK_EXPIRE_AFTER"])
TRANSACTION_TRACK_ID_EXPIRE_AFTER = 3600  # 1 hour

HEARTBEAT_INTERVAL = 60

MAX_ACTIONS_LENGTH = 30

RABBITMQ_PORT = os.environ["RABBITMQ_PORT"]
RABBITMQ_UI_PORT = os.environ["RABBITMQ_UI_PORT"]
RABBITMQ_USER = os.environ["RABBITMQ_USER"]
RABBITMQ_PASS = os.environ["RABBITMQ_PASS"]
RABBITMQ_HOST = os.environ["RABBITMQ_HOST"]

MESSAGES_BROKER_URL = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/"

EVENTS_EXCHANGE_NAME = os.environ.get("EVENTS_EXCHANGE_NAME", "events")
EVENTS_QUEUE_NAME = os.environ.get("EVENTS_QUEUE_NAME", "events")
TASKS_EXCHANGE_NAME = os.environ.get("TASKS_EXCHANGE_NAME", "tasks")
MAX_MESSAGE_PRIORITY = 10
REGULAR_MESSAGE_PRIORITY = 5
LOW_MESSAGE_PRIORITY = 1
LOG_FILEPATH = os.environ["LOG_FILEPATH"]
HTTP_SERVER_HOST = os.environ["HTTP_SERVER_HOST"]
HTTP_SERVER_PORT = int(os.environ["HTTP_SERVER_PORT"])
OCPP_VERSION = os.environ["OCPP_VERSION"]

CHARGE_POINT_ID_HEADER_NAME = "Charge-Point-Id"
