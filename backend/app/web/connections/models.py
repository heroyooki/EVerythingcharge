from sqlalchemy import (
    Column,
    String,
    Integer, Boolean
)
from sqlalchemy.dialects.postgresql import JSONB

from core.models import Model


class Connection(Model):
    __tablename__ = "connections"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String, nullable=True)
    reason = Column(String, nullable=True)
    custom_data = Column(JSONB, default=dict)

    master_id = Column(String(36), nullable=False)
    is_active = Column(Boolean, default=False)
