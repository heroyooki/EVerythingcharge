from __future__ import annotations

from typing import Dict, Any

from loguru import logger

from api.web.sse import observer as obs


class Publisher:
    observers: Dict[str, obs.Observer] = {}
    view = None

    def __init__(self, service: Any, *args, **kwargs):
        self.service = service

    async def notify_observer(
            self,
            observer_id: str,
            event: Dict
    ) -> None:
        observer = self.observers.get(observer_id)
        if observer:
            await observer.put_event(event)
            logger.info(f"An observer was notified (network_id={observer.network_id}, event={event})")

    async def ensure_observers(self) -> None:
        """
        Remove inactive observers from the 'observers' list.
        :return:
        """
        self.observers = {k: v for k, v in self.observers.items() if not await v.request.is_disconnected()}

    async def add_observer(self, observer: obs.Observer) -> None:
        await self.ensure_observers()
        self.observers[observer.id] = observer
        logger.info(f"Added new observer (network_id={observer.network_id}, user={observer.id})")

    async def remove_observer(self, observer: obs.Observer) -> None:
        self.observers.pop(observer.id, None)
        logger.info(f"Removed observer (network_id={observer.network_id})")
