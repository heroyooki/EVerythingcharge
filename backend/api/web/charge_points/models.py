from __future__ import annotations

from sqlalchemy import (
    Column,
    String,
    ForeignKey, Integer, UniqueConstraint, PrimaryKeyConstraint
)
from sqlalchemy.orm import relationship

from api.web.networks.models import Network
from core.models import Model


class ChargePoint(Model):
    __tablename__ = "charge_points"

    description = Column(String(124), nullable=True)
    vendor = Column(String, nullable=True)
    serial_number = Column(String, nullable=True)
    location = Column(String, nullable=True)
    model = Column(String, nullable=True)

    network_id = Column(String, ForeignKey("networks.id"), nullable=True)
    network = relationship(Network, back_populates="charge_points", lazy="joined")
    connectors = relationship("Connector",
                              back_populates="charge_point",
                              passive_deletes=True,
                              lazy="joined",
                              order_by="Connector.id")
    configurations = relationship("Configuration", back_populates="charge_point", lazy="joined")
    connection = relationship("Connection", back_populates="charge_point", lazy="joined", uselist=False)

    def __repr__(self):
        return f"ChargePoint (id={self.id}, location={self.location})"


class Connection(Model):
    __tablename__ = "connections"

    status = Column(String, nullable=True)
    error_code = Column(String, nullable=True)

    charge_point_id = Column(String, ForeignKey("charge_points.id", ondelete='CASCADE'), nullable=False)
    charge_point = relationship("ChargePoint", back_populates="connection", lazy="noload")


class Configuration(Model):
    __tablename__ = "configurations"

    __table_args__ = (
        UniqueConstraint("key", "charge_point_id"),
    )

    key = Column(String, nullable=False)
    value = Column(String, nullable=False)

    charge_point_id = Column(String, ForeignKey("charge_points.id", ondelete='CASCADE'), nullable=False)
    charge_point = relationship("ChargePoint", back_populates="configurations", lazy="joined")

    def __repr__(self):
        return f"Configuration (key={self.key}, value={self.value})"


class Connector(Model):
    __tablename__ = "connectors"

    __table_args__ = (
        PrimaryKeyConstraint("id", "charge_point_id"),
    )

    id = Column(Integer, nullable=False)
    status = Column(String, index=True, nullable=False)
    error_code = Column(String, nullable=True)

    charge_point_id = Column(String, ForeignKey("charge_points.id", ondelete='CASCADE'), nullable=False)
    charge_point = relationship("ChargePoint", back_populates="connectors", lazy="joined")
