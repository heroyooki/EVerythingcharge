from __future__ import annotations

from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    UniqueConstraint, SmallInteger
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.web.connections.models import Connection
from app.web.grids.models import Grid
from app.web.locations.models import Location
from core.models import Model


class ChargePoint(Model):
    __tablename__ = "charge_points"
    __table_args__ = (
        UniqueConstraint("grid_id", "id"),
    )

    id = Column(String(20), primary_key=True)
    vendor_name = Column(String, nullable=True)
    model = Column(String, nullable=True)
    serial_number = Column(String, nullable=True)
    firmware_version = Column(String, nullable=True)
    custom_data = Column(JSONB, default=dict)

    grid_id = Column(String, ForeignKey("grids.id", ondelete='SET NULL'), nullable=False)
    grid = relationship(Grid, back_populates="charge_points", lazy="joined")
    location = relationship(
        Location,
        foreign_keys=[Location.master_id],
        primaryjoin="ChargePoint.id==Location.master_id",
        lazy="joined",
        uselist=False,
        viewonly=True
    )
    connection = relationship(
        Connection,
        foreign_keys=[Connection.master_id],
        primaryjoin="ChargePoint.id==Connection.master_id",
        lazy="joined",
        uselist=False,
        viewonly=True
    )
    evses = relationship("EVSE", back_populates="charge_point", lazy="joined")


class EVSE(Model):
    __tablename__ = "evses"
    __table_args__ = (
        UniqueConstraint("order_id", "charge_point_id"),
    )

    order_id = Column(SmallInteger, autoincrement=True)
    charge_point_id = Column(String, ForeignKey("charge_points.id", ondelete='CASCADE'), nullable=False)
    charge_point = relationship("ChargePoint", back_populates="evses", lazy="joined")
    connectors = relationship("Connector",
                              back_populates="evse",
                              passive_deletes=True,
                              lazy="joined",
                              order_by="Connector.id")
    connection = relationship(
        Connection,
        foreign_keys=[Connection.master_id],
        primaryjoin="EVSE.id==Connection.master_id",
        lazy="joined",
        uselist=False,
        viewonly=True
    )


class Connector(Model):
    __tablename__ = "connectors"

    __table_args__ = (
        UniqueConstraint("order_id", "evse_id"),
    )

    order_id = Column(SmallInteger, autoincrement=True)
    evse_id = Column(String, ForeignKey("evses.id", ondelete='CASCADE'), nullable=False)
    evse = relationship("EVSE", back_populates="connectors", lazy="joined")

    connection = relationship(
        Connection,
        foreign_keys=[Connection.master_id],
        primaryjoin="Connector.id==Connection.master_id",
        lazy="joined",
        uselist=False,
        viewonly=True
    )
