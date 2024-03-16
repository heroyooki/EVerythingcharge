from __future__ import annotations

from sqlalchemy import (
    Column,
    String,
    ForeignKey
)
from sqlalchemy.orm import relationship

from api.web.networks.models import Network
from core.models import Model


class ChargePoint(Model):
    __tablename__ = "charge_points"

    description = Column(String(124), nullable=True)
    status = Column(String, index=True, nullable=False)
    vendor = Column(String, nullable=True)
    serial_number = Column(String, nullable=True)
    location = Column(String, nullable=True)
    model = Column(String, nullable=True)
    ocpp_version = Column(String, nullable=False)

    network_id = Column(String, ForeignKey("networks.id"), nullable=False)
    network = relationship(Network, back_populates="charge_points", lazy="joined")

    def __repr__(self):
        return f"ChargePoint (id={self.id}, status={self.status}, location={self.location})"
