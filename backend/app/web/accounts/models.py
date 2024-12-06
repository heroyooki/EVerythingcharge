from sqlalchemy import (
    Column,
    String
)
from sqlalchemy.orm import relationship

from core.models import Model


class Account(Model):
    __tablename__ = "accounts"

    name = Column(String, nullable=False, unique=True)

    grids = relationship("Grid", back_populates="account", lazy="joined")
