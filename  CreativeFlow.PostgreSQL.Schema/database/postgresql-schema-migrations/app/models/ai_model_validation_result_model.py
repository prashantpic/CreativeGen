import uuid
from sqlalchemy import (
    Column, DateTime, String, ForeignKey, CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..db.base import Base


class AIModelValidationResult(Base):
    """
    Stores results from validating an AI model version.
    """
    __tablename__ = 'ai_model_validation_results'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    modelVersionId = Column(UUID(as_uuid=True), ForeignKey('ai_model_versions.id', ondelete='CASCADE'), nullable=False, unique=True, index=True)
    validationTimestamp = Column(DateTime, nullable=False, server_default=func.now(), index=True)
    securityScanStatus = Column(String(50), nullable=False)
    functionalStatus = Column(String(50), nullable=False)
    performanceBenchmark = Column(JSONB, nullable=True)
    results = Column(JSONB, nullable=True)
    validatedByUserId = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    createdAt = Column(DateTime, nullable=False, server_default=func.now())

    # Relationships
    model_version = relationship("AIModelVersion", foreign_keys=[modelVersionId])
    validated_by_user = relationship("User", foreign_keys=[validatedByUserId], back_populates="validated_model_results")

    __table_args__ = (
        CheckConstraint(securityScanStatus.in_(['Passed', 'Failed', 'Pending', 'Skipped']), name='ck_validation_result_security_status'),
        CheckConstraint(functionalStatus.in_(['Passed', 'Failed', 'Pending', 'Skipped']), name='ck_validation_result_functional_status'),
    )

    def __repr__(self):
        return f"<AIModelValidationResult(id={self.id}, modelVersionId='{self.modelVersionId}')>"