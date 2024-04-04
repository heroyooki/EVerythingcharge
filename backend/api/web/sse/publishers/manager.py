from __future__ import annotations

from api.web.charge_points import service
from api.web.sse.publishers.charge_points import ChargePointPublisher


class PublishingManager:
    charge_point_publisher = ChargePointPublisher(service)
