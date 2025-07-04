"""
SQLAlchemy ORM model for AI Models.

This file defines the database table structure for the 'aimodels' table,
which stores metadata for AI models available on the platform.
"""
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class AIModelORM(Base):
    """
    SQLAlchemy ORM model for the `aimodels` table.

    This class maps to the `aimodels` table in the PostgreSQL database.
    It includes columns for model metadata and defines a one-to-many
    relationship with its versions.
    """
    __tablename__ = "aimodels"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    task_type = Column(String(50), nullable=False, index=True)
    owner_id = Column(UUID(as_uuid=True), nullable=True)  # FK to User or Team in another service
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    versions = relationship("AIModelVersionORM", back_populates="model", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<AIModelORM(id={self.id}, name='{self.name}')>"