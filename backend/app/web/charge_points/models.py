from __future__ import annotations

from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    UniqueConstraint,
    PrimaryKeyConstraint,
    SmallInteger
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
    vendor_name = Column(String, nullable=False)
    serial_number = Column(String, nullable=True)
    model = Column(String, nullable=False)
    firmware_version = Column(String, nullable=True)

    grid_id = Column(String, ForeignKey("grids.id", ondelete='SET NULL'), nullable=False)
    grid = relationship(Grid, back_populates="charge_points", lazy="joined")
    configurations = relationship("Configuration", back_populates="charge_point", lazy="joined")
    location = relationship(
        Location,
        foreign_keys=[Location.master_id],
        primaryjoin="ChargePoint.id==Location.master_id",
        lazy="joined",
        uselist=False
    )
    connection = relationship(
        Connection,
        foreign_keys=[Connection.master_id],
        primaryjoin="ChargePoint.id==Connection.master_id",
        lazy="joined",
        uselist=False
    )
    evses = relationship("EVSE", back_populates="charge_point", lazy="joined")

    def __repr__(self):
        return f"ChargePoint (id={self.id}, location={self.location})"


class EVSE(Model):
    __tablename__ = "evses"
    __table_args__ = (
        PrimaryKeyConstraint("id", "charge_point_id"),
    )

    id = Column(String(20), primary_key=True)
    custom_data = Column(JSONB, default=dict)

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
        uselist=False
    )


class Connector(Model):
    __tablename__ = "connectors"

    __table_args__ = (
        PrimaryKeyConstraint("id", "evse_id"),
    )

    id = Column(String(20), primary_key=True)
    status = Column(String, index=True, nullable=False)
    reason = Column(String, nullable=True)
    custom_data = Column(JSONB, default=dict)

    evse_id = Column(String, ForeignKey("evses.id", ondelete='CASCADE'), nullable=False)
    evse = relationship("EVSE", back_populates="connectors", lazy="joined")

    connection = relationship(
        Connection,
        foreign_keys=[Connection.master_id],
        primaryjoin="Connector.id==Connection.master_id",
        lazy="joined",
        uselist=False
    )


class Configuration(Model):
    __tablename__ = "configurations"

    __table_args__ = (
        UniqueConstraint("key", "charge_point_id"),
    )

    id = Column(SmallInteger, primary_key=True)
    key = Column(String, nullable=False)
    value = Column(String, nullable=False)

    charge_point_id = Column(String, ForeignKey("charge_points.id", ondelete='CASCADE'), nullable=False)
    charge_point = relationship("ChargePoint", back_populates="configurations", lazy="joined")

    def __repr__(self):
        return f"Configuration (key={self.key}, value={self.value})"
