from sqlalchemy import (
    Column,
    String
)
from sqlalchemy.orm import relationship

from core.models import Model


class Network(Model):
    __tablename__ = "networks"

    name = Column(String, nullable=False, unique=True)
    location = Column(String, nullable=False)

    charge_points = relationship("ChargePoint",
                                 back_populates="network",
                                 lazy="joined")
