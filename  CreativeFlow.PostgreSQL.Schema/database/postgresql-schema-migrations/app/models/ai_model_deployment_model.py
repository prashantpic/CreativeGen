import uuid
from sqlalchemy import (
    Column, DateTime, String, ForeignKey, CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..db.base import Base


class AIModelDeployment(Base):
    """
    Records deployments of AI model versions to various environments.
    """
    __tablename__ = 'ai_model_deployments'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    modelVersionId = Column(UUID(as_uuid=True), ForeignKey('ai_model_versions.id', ondelete='CASCADE'), nullable=False, index=True)
    environment = Column(String(50), nullable=False, index=True)
    status = Column(String(50), nullable=False, default='Initiated', index=True)
    deploymentStrategy = Column(String(50), nullable=True)
    endpoint = Column(String(255), nullable=True)
    kubernetesDetails = Column(JSONB, nullable=True)
    deployedByUserId = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    deploymentTimestamp = Column(DateTime, nullable=False, server_default=func.now())
    createdAt = Column(DateTime, nullable=False, server_default=func.now())
    updatedAt = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Relationships
    model_version = relationship("AIModelVersion", back_populates="deployments")
    deployed_by_user = relationship("User", foreign_keys=[deployedByUserId], back_populates="deployed_model_versions")

    __table_args__ = (
        CheckConstraint(environment.in_(['staging', 'production', 'testing']), name='ck_ai_model_deployment_environment'),
        CheckConstraint(status.in_(['Initiated', 'Deploying', 'Active', 'Inactive', 'Failed', 'RolledBack']), name='ck_ai_model_deployment_status'),
    )

    def __repr__(self):
        return f"<AIModelDeployment(id={self.id}, modelVersionId='{self.modelVersionId}', env='{self.environment}')>"