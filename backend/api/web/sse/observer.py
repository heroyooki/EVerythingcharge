from __future__ import annotations

import asyncio
from typing import Dict

from loguru import logger

counter = []


class Observer(asyncio.Queue):
    # To prevent memory overflow
    max_events_count = 10

    def __init__(self, request, network_id, *args, **kwargs):
        super().__init__(*args, **kwargs, maxsize=self.max_events_count)
        self.id = request.user.id
        self.request = request
        self.network_id = network_id

    async def subscribe(self, publisher) -> None:
        await publisher.add_observer(self)
        logger.info(
            f"Subscribing a new observer (network_id={self.network_id}, observers={publisher.observers.keys()})")

    async def unsubscribe(self, publisher) -> None:
        await publisher.remove_observer(self)
        logger.info(f"Unsubscribed observer (network_id={self.network_id})")

    async def put_event(self, event: Dict) -> None:
        await self.put(event)
        logger.info(f"A new event was put (network_id={self.network_id}, event={event})")

    async def consume_event(self) -> str:
        return await self.get()
