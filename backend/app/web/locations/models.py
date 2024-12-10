from sqlalchemy import (
    Column,
    String,
    Numeric
)

from core.models import Model


class Location(Model):
    __tablename__ = "locations"

    latitude = Column(Numeric, nullable=True)
    longitude = Column(Numeric, nullable=True)
    city = Column(String, nullable=True)
    address = Column(String, nullable=True)

    master_id = Column(String(36), nullable=False)
