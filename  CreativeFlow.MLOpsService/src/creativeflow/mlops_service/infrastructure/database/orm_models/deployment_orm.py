"""
SQLAlchemy ORM model for the `aimodeldeployments` table.
"""
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from . import Base


class AIModelDeploymentORM(Base):
    """
    SQLAlchemy ORM class for AI Model Deployments.

    Maps to the `aimodeldeployments` table in the PostgreSQL database.
    """
    __tablename__ = "aimodeldeployments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    model_version_id = Column(UUID(as_uuid=True), ForeignKey("aimodelversions.id"), nullable=False, index=True)
    environment = Column(String(50), index=True, nullable=False)
    status = Column(String(50), index=True, nullable=False)
    deployment_strategy = Column(String(50), nullable=True)
    endpoint_url = Column(String, nullable=True)
    replicas = Column(Integer, nullable=True)
    config = Column(JSONB, nullable=True)
    deployed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    deployed_by_user_id = Column(UUID(as_uuid=True), nullable=True)

    # Relationships
    model_version = relationship("AIModelVersionORM", back_populates="deployments")