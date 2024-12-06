from sqlalchemy import (
    Column,
    String, ForeignKey, BigInteger
)
from sqlalchemy.orm import relationship

from core.models import Model


class Grid(Model):
    __tablename__ = "grids"

    name = Column(String, nullable=False, unique=True)
    capacity = Column(BigInteger, nullable=True)
    unit = Column(String, nullable=False)
    supplier = Column(String, nullable=False)

    account_id = Column(String, ForeignKey("accounts.id", ondelete='CASCADE'), nullable=False)
    account = relationship("Account", back_populates="grids", lazy="joined")

    charge_points = relationship("ChargePoint", back_populates="grid", lazy="joined")
