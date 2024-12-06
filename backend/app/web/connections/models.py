from sqlalchemy import (
    Column,
    String,
    SmallInteger
)
from sqlalchemy.dialects.postgresql import JSONB

from core.models import Model


class Connection(Model):
    __tablename__ = "connections"

    id = Column(SmallInteger, primary_key=True)
    status = Column(String, nullable=True)
    reason = Column(String, nullable=True)
    custom_data = Column(JSONB, default=dict)

    master_id = Column(String, nullable=False)
