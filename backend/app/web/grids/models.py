from sqlalchemy import (
    Column,
    String, ForeignKey, BigInteger, UniqueConstraint
)
from sqlalchemy.orm import relationship

from app.web.accounts.models import Account
from app.web.locations.models import Location
from core.models import Model


class Grid(Model):
    __tablename__ = "grids"
    __table_args__ = (
        UniqueConstraint("account_id", "name"),
    )

    name = Column(String, nullable=False)
    capacity = Column(BigInteger, nullable=False)
    unit = Column(String, nullable=False)
    supplier = Column(String, nullable=False)

    account_id = Column(String, ForeignKey("accounts.id", ondelete='CASCADE'), nullable=False)
    account = relationship(Account, back_populates="grids", lazy="joined")

    charge_points = relationship("ChargePoint", back_populates="grid", lazy="joined")

    location = relationship(
        Location,
        foreign_keys=[Location.master_id],
        primaryjoin="Grid.id==Location.master_id",
        lazy="joined",
        uselist=False,
        viewonly=True
    )
