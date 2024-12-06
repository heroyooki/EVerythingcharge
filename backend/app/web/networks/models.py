from sqlalchemy import (
    Column,
    String
)

from core.models import Model


class Network(Model):
    __tablename__ = "networks"

    name = Column(String, nullable=False, unique=True)
    location = Column(String, nullable=False)
