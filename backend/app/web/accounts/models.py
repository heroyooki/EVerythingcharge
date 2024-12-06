from sqlalchemy import (
    Column,
    String
)
from sqlalchemy.orm import relationship

from app.web.locations.models import Location
from core.models import Model


class Account(Model):
    __tablename__ = "accounts"

    name = Column(String, nullable=False, unique=True)

    grids = relationship("Grid", back_populates="account", lazy="joined")
    location = relationship(
        Location,
        foreign_keys=[Location.master_id],
        primaryjoin="Account.id==Location.master_id",
        lazy="joined",
        uselist=False
    )
