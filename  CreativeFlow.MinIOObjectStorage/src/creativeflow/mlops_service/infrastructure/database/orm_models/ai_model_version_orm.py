"""
SQLAlchemy ORM model for AI Model Versions.

This file defines the database table structure for the 'aimodelversions' table,
which stores metadata for specific versions of AI models.
"""
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from .ai_model_orm import Base


class AIModelVersionORM(Base):
    """
    SQLAlchemy ORM model for the `aimodelversions` table.

    This class maps to the `aimodelversions` table in the PostgreSQL database.
    It includes details about a specific model version, its artifact, status,
    and relationships to its parent model, deployments, validation results,
    and feedback.
    """
    __tablename__ = "aimodelversions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    model_id = Column(UUID(as_uuid=True), ForeignKey("aimodels.id"), nullable=False, index=True)
    version_string = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    artifact_path = Column(String(1024), nullable=False)
    model_format = Column(String(50), nullable=False)
    interface_type = Column(String(50), nullable=False)
    parameters = Column(JSONB, nullable=True)
    metrics = Column(JSONB, nullable=True)
    status = Column(String(50), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_by_user_id = Column(UUID(as_uuid=True), nullable=True)

    # Relationships
    model = relationship("AIModelORM", back_populates="versions")
    deployments = relationship("AIModelDeploymentORM", back_populates="model_version", cascade="all, delete-orphan")
    validation_results = relationship("AIModelValidationResultORM", back_populates="model_version", cascade="all, delete-orphan")
    feedbacks = relationship("AIModelFeedbackORM", back_populates="model_version", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<AIModelVersionORM(id={self.id}, model_id={self.model_id}, version='{self.version_string}')>"