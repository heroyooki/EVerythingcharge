from __future__ import annotations

from sqlalchemy import (
    Column,
    String
)

from core.models import Model


class User(Model):
    __tablename__ = "users"

    password = Column(String(124), nullable=True, unique=False)
    email = Column(String(48), nullable=False, unique=True)
    first_name = Column(String(24), nullable=False, unique=False)
    last_name = Column(String(24), nullable=False, unique=False)

    def __repr__(self) -> str:
        return f"User: {self.id}, {self.email}, {self.role}"
