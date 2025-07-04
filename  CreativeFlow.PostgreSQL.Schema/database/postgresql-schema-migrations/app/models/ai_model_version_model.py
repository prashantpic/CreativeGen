import uuid
from sqlalchemy import (
    Column, DateTime, String, ForeignKey, Text, CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.schema import UniqueConstraint

from ..db.base import Base


class AIModelVersion(Base):
    """
    Stores specific versions of AI models, their source, and status.
    """
    __tablename__ = 'ai_model_versions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    modelId = Column(UUID(as_uuid=True), ForeignKey('ai_models.id', ondelete='CASCADE'), nullable=False, index=True)
    versionNumber = Column(String(50), nullable=False)
    sourcePath = Column(String(1024), nullable=True)
    format = Column(String(50), nullable=True)
    parameters = Column(JSONB, nullable=True)
    status = Column(String(50), nullable=False, default='Staged', index=True)
    validationResultId = Column(UUID(as_uuid=True), ForeignKey('ai_model_validation_results.id', ondelete='SET NULL'), nullable=True)
    createdByUserId = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    releaseNotes = Column(Text, nullable=True)
    createdAt = Column(DateTime, nullable=False, server_default=func.now())
    updatedAt = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Relationships
    ai_model_parent = relationship("AIModel", back_populates="versions")
    created_by_user = relationship("User", foreign_keys=[createdByUserId], back_populates="created_model_versions")
    
    # A version can have one current validation result linked
    validation_result = relationship("AIModelValidationResult", foreign_keys=[validationResultId])

    # A version can be deployed multiple times
    deployments = relationship("AIModelDeployment", back_populates="model_version", cascade="all, delete-orphan")
    feedbacks = relationship("AIModelFeedback", back_populates="model_version")

    __table_args__ = (
        UniqueConstraint('modelId', 'versionNumber', name='uq_aimodelversion_model_version'),
        CheckConstraint(status.in_(['Staged', 'Production', 'Deprecated', 'Archived', 'Failed']), name='ck_ai_model_version_status'),
    )

    def __repr__(self):
        return f"<AIModelVersion(id={self.id}, modelId='{self.modelId}', version='{self.versionNumber}')>"