"""
SQLAlchemy ORM model for Model Deployments.

This file defines the database table structure for the 'aimodeldeployments' table,
which tracks the deployment of AI model versions to different environments.
"""
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from .ai_model_orm import Base


class AIModelDeploymentORM(Base):
    """
    SQLAlchemy ORM model for the `aimodeldeployments` table.

    This class maps to the `aimodeldeployments` table in the PostgreSQL database.
    It records information about each deployment instance, including its target
    environment, status, strategy, and configuration.
    """
    __tablename__ = "aimodeldeployments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    model_version_id = Column(UUID(as_uuid=True), ForeignKey("aimodelversions.id"), nullable=False, index=True)
    environment = Column(String(50), nullable=False, index=True)
    status = Column(String(50), nullable=False, index=True)
    deployment_strategy = Column(String(50), nullable=True)
    endpoint_url = Column(String(255), nullable=True)
    replicas = Column(Integer, nullable=True)
    config = Column(JSONB, nullable=True)  # For K8s details, traffic split, etc.
    deployed_at = Column(DateTime, nullable=True)
    deployed_by_user_id = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    model_version = relationship("AIModelVersionORM", back_populates="deployments")

    def __repr__(self):
        return f"<AIModelDeploymentORM(id={self.id}, version_id={self.model_version_id}, env='{self.environment}')>"