from __future__ import annotations

from ocpp.v201.enums import ConnectorStatusType
from propan import Context
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    UniqueConstraint, SmallInteger
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.web.connections.models import Connection
from app.web.connections.service import update_connection
from app.web.connections.views import ConnectionView
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

    def get_evse(self, order_id: int) -> "EVSE":
        return next((i for i in self.evses if i.order_id == order_id), None)

    def has_evse(self, order_id: int):
        return bool(self.get_evse(order_id))


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

    def get_connector(self, order_id: int) -> "Connector":
        return next((i for i in self.connectors if i.order_id == order_id), None)

    def has_connector(self, order_id: int):
        return bool(self.get_connector(order_id))


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

    async def apply_status(self, status: ConnectorStatusType, status_mapper=Context()):
        """
        The Charging Station sends StatusNotificationRequest to the CSMS for each Connector.
        If the status was set to Unavailable or Reserved from the CSMS prior to the (re)boot,
        the Connector should return to this status, otherwise, the status should be Available or,
        when it resumes a transaction that was ongoing, the status should be Occupied.
        """
        status = status_mapper.get(self.connection.status, status)
        data = ConnectionView(status=status)
        await update_connection(self.id, data.model_dump(exclude_unset=True))


HTTP_STATUS_MAPPER = {}
AMQP_STATUS_MAPPER = {
    ConnectorStatusType.unavailable: ConnectorStatusType.unavailable,
    ConnectorStatusType.occupied: ConnectorStatusType.occupied,
    ConnectorStatusType.reserved: ConnectorStatusType.reserved
}
