import uuid
from sqlalchemy import (
    Column, DateTime, String, ForeignKey, Text, DECIMAL, Integer, CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..db.base import Base


class GenerationRequest(Base):
    """
    Tracks AI creative generation requests, inputs, status, and outputs.
    """
    __tablename__ = 'generation_requests'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userId = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='RESTRICT'), nullable=False, index=True)
    projectId = Column(UUID(as_uuid=True), ForeignKey('projects.id', ondelete='SET NULL'), nullable=False, index=True)
    inputPrompt = Column(Text, nullable=False)
    styleGuidance = Column(Text, nullable=True)
    inputParameters = Column(JSONB, nullable=True)
    status = Column(String(50), nullable=False, default='Pending', index=True)
    errorMessage = Column(Text, nullable=True)
    sampleAssets = Column(JSONB, nullable=True)
    selectedSampleId = Column(UUID(as_uuid=True), ForeignKey('assets.id', ondelete='SET NULL'), nullable=True)
    finalAssetId = Column(UUID(as_uuid=True), ForeignKey('assets.id', ondelete='SET NULL'), nullable=True)
    creditsCostSample = Column(DECIMAL(10, 2), nullable=True)
    creditsCostFinal = Column(DECIMAL(10, 2), nullable=True)
    aiModelUsed = Column(String(100), nullable=True)
    processingTimeMs = Column(Integer, nullable=True)
    createdAt = Column(DateTime, nullable=False, server_default=func.now(), index=True)
    updatedAt = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="generation_requests")
    project = relationship("Project", back_populates="generation_requests")
    
    selected_sample = relationship("Asset", foreign_keys=[selectedSampleId])
    final_asset = relationship("Asset", foreign_keys=[finalAssetId])

    credit_transactions = relationship("CreditTransaction", back_populates="generation_request")
    usage_logs = relationship("UsageLog", back_populates="generation_request")
    feedbacks = relationship("AIModelFeedback", back_populates="generation_request")
    
    __table_args__ = (
        CheckConstraint(status.in_([
            'Pending', 'ProcessingSamples', 'AwaitingSelection', 'ProcessingFinal',
            'Completed', 'Failed', 'Cancelled', 'ContentRejected'
        ]), name='ck_generation_request_status'),
    )

    def __repr__(self):
        return f"<GenerationRequest(id={self.id}, status='{self.status}')>"