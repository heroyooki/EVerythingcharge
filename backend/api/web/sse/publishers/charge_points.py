from __future__ import annotations

from propan import apply_types, Context

from api.web.charge_points.models import ChargePoint
from api.web.charge_points.views import ChargePointView
from api.web.sse.publishers.base import Publisher


class ChargePointPublisher(Publisher):
    view = ChargePointView

    @apply_types
    async def publish(
            self_,
            charge_point: ChargePoint,
            session=Context()
    ):
        """
        Publish new event for all observers in the list
        :param func:
        :return:
        """
        await session.refresh(charge_point)

        for key in self_.observers.keys():
            if self_.observers[key].network_id == charge_point.network_id:
                await self_.notify_observer(
                    key,
                    {
                        "event": "message",
                        "data": self_.view.from_orm(charge_point).json()
                    }
                )
