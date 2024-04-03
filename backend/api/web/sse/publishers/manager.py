from __future__ import annotations

from api.web.charge_points import service
from api.web.sse.publishers.charge_points import SimpleChargePointPublisher, DetailedChargePointPublisher


class PublishingManager:
    simple_charge_point_publisher = SimpleChargePointPublisher(service)
    detailed_charge_point_publisher = DetailedChargePointPublisher(service)
