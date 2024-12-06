from sqlalchemy import (
    Column,
    String,
    REAL
)

from core.models import Model


class Location(Model):
    __tablename__ = "locations"

    latitude = Column(REAL, nullable=True)
    longitude = Column(REAL, nullable=True)
    city = Column(String, nullable=True)
    address = Column(String, nullable=True)

    master_id = Column(String, nullable=False)
