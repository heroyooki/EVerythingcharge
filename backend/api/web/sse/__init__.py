import asyncio

from fastapi import Request

from api.web.sse.observer import Observer
from api.web.sse.publishers.manager import PublishingManager

_sse_publisher: PublishingManager | None = None


async def event_generator(observer: Observer):
    delay = 0.5  # seconds

    while True:
        event = await observer.consume_event()
        if event is not None:
            yield event
        await asyncio.sleep(delay)


def get_sse_publisher():
    global _sse_publisher
    if not _sse_publisher:
        _sse_publisher = PublishingManager()
    return _sse_publisher


async def get_event_generator():
    return event_generator


async def get_observer(request: Request, network_id):
    return Observer(request, network_id)
