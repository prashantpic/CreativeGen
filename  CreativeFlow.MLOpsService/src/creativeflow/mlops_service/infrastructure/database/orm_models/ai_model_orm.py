"""
SQLAlchemy ORM model for the `aimodels` table.
"""
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from . import Base


class AIModelORM(Base):
    """

    SQLAlchemy ORM class for AI Models.

    Maps to the `aimodels` table in the PostgreSQL database.
    """
    __tablename__ = "aimodels"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    task_type = Column(String(50), index=True, nullable=False)
    owner_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    versions = relationship("AIModelVersionORM", back_populates="model", cascade="all, delete-orphan")