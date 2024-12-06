from sqlalchemy import (
    Column,
    String,
    Float
)

from core.models import Model


class Location(Model):
    __tablename__ = "locations"

    latitude = Column(Float(5), nullable=True)
    longitude = Column(Float(5), nullable=True)
    city = Column(String, nullable=True)
    address = Column(String, nullable=True)

    master_id = Column(String, nullable=False)
