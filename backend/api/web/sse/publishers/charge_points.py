from __future__ import annotations

from typing import Union

from api.web.charge_points.models import ChargePoint
from api.web.charge_points.views import SimpleChargePoint, ChargePointView
from api.web.sse.publishers.base import Publisher
from core.models import get_contextual_session


class ChargePointPublisher(Publisher):

    async def publish(self, identity: Union[str, ChargePoint]):
        """
        Publish new event for all observers in the list
        :param func:
        :return:
        """
        async with get_contextual_session() as session:
            if isinstance(identity, str):
                charge_point = await self.service.get_charge_point(identity, session=session)
            if isinstance(identity, ChargePoint):
                charge_point = identity
            for key in self.observers.keys():
                if self.observers[key].network_id == charge_point.network_id:
                    await self.notify_observer(
                        key,
                        {
                            "event": "message",
                            "data": self.view.from_orm(charge_point).json()
                        }
                    )


class SimpleChargePointPublisher(ChargePointPublisher):
    view = SimpleChargePoint


class DetailedChargePointPublisher(ChargePointPublisher):
    view = ChargePointView
