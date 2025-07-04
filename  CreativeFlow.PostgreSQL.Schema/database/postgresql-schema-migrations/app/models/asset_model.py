import uuid
from sqlalchemy import (
    Boolean, Column, DateTime, String, ForeignKey, CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..db.base import Base


class Asset(Base):
    """
    Represents an uploaded or AI-generated creative asset file.
    """
    __tablename__ = 'assets'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    projectId = Column(UUID(as_uuid=True), ForeignKey('projects.id', ondelete='SET NULL'), nullable=True, index=True)
    userId = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    generationRequestId = Column(UUID(as_uuid=True), ForeignKey('generation_requests.id', ondelete='SET NULL'), nullable=True, index=True)
    name = Column(String(255), nullable=False)
    type = Column(String(20), nullable=False, index=True)
    filePath = Column(String(1024), nullable=False)
    mimeType = Column(String(50), nullable=False)
    format = Column(String(10), nullable=False)
    resolution = Column(String(20), nullable=True)
    isFinal = Column(Boolean, nullable=False, default=False)
    metadata = Column(JSONB, nullable=True)
    createdAt = Column(DateTime, nullable=False, server_default=func.now(), index=True)
    updatedAt = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deletedAt = Column(DateTime, nullable=True, index=True)

    # Relationships
    project = relationship("Project", back_populates="assets")
    user = relationship("User", back_populates="assets")
    
    # An asset can be linked from a generation request, but the main relationship
    # is defined on GenerationRequest to Asset (finalAssetId, selectedSampleId)
    # This FK allows finding the source request for a given asset.
    generation_request_source = relationship("GenerationRequest", foreign_keys=[generationRequestId])

    versions = relationship("AssetVersion", back_populates="asset", cascade="all, delete-orphan")
    
    __table_args__ = (
        CheckConstraint(type.in_(['Uploaded', 'AIGenerated', 'Derived']), name='ck_asset_type'),
    )

    def __repr__(self):
        return f"<Asset(id={self.id}, name='{self.name}')>"