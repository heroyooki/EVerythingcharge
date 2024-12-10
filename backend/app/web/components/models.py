from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from core.models import Model


class Component(Model):
    __tablename__ = "components"

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    parent_id = Column(String, ForeignKey("components.id", ondelete="CASCADE"), nullable=True)
    master_id = Column(String(36), nullable=True)

    variables = relationship("Variable", back_populates="component", lazy="joined")


class Variable(Model):
    __tablename__ = "variables"

    component_id = Column(String, ForeignKey("components.id", ondelete="CASCADE"), nullable=False)
    description = Column(String, nullable=True)
    name = Column(String, nullable=False)
    value = Column(String, nullable=False)
    type = Column(String, nullable=False)

    component = relationship("Component", back_populates="variables", lazy="joined")
