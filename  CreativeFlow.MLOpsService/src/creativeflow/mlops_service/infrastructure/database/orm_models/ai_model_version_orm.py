"""
SQLAlchemy ORM model for the `aimodelversions` table.
"""
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from creativeflow.mlops_service.domain.enums import ModelVersionStatusEnum

from . import Base


class AIModelVersionORM(Base):
    """
    SQLAlchemy ORM class for AI Model Versions.

    Maps to the `aimodelversions` table in the PostgreSQL database.
    """
    __tablename__ = "aimodelversions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    model_id = Column(UUID(as_uuid=True), ForeignKey("aimodels.id"), nullable=False, index=True)
    version_string = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    artifact_path = Column(String, nullable=False)
    model_format = Column(String(50), nullable=False)
    interface_type = Column(String(50), nullable=False)
    parameters = Column(JSONB, nullable=True)
    metrics = Column(JSONB, nullable=True)
    status = Column(String(50), index=True, nullable=False, default=ModelVersionStatusEnum.STAGING.value)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_by_user_id = Column(UUID(as_uuid=True), nullable=True)

    # Relationships
    model = relationship("AIModelORM", back_populates="versions")
    deployments = relationship("AIModelDeploymentORM", back_populates="model_version", cascade="all, delete-orphan")
    validation_results = relationship("AIModelValidationResultORM", back_populates="model_version", cascade="all, delete-orphan")
    feedbacks = relationship("AIModelFeedbackORM", back_populates="model_version", cascade="all, delete-orphan")