import uuid
from sqlalchemy import (
    Column, DateTime, String, ForeignKey, Integer, Text
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..db.base import Base


class AssetVersion(Base):
    """
    Stores version history for creative assets or project states.
    """
    __tablename__ = 'asset_versions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assetId = Column(UUID(as_uuid=True), ForeignKey('assets.id', ondelete='CASCADE'), nullable=True, index=True)
    projectId = Column(UUID(as_uuid=True), ForeignKey('projects.id', ondelete='CASCADE'), nullable=True, index=True)
    versionNumber = Column(Integer, nullable=False)
    filePath = Column(String(1024), nullable=True)
    stateData = Column(JSONB, nullable=True)
    description = Column(Text, nullable=True)
    createdByUserId = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    createdAt = Column(DateTime, nullable=False, server_default=func.now())

    # Relationships
    asset = relationship("Asset", back_populates="versions")
    project = relationship("Project", back_populates="versions")
    created_by_user = relationship("User", foreign_keys=[createdByUserId])

    def __repr__(self):
        return f"<AssetVersion(id={self.id}, versionNumber={self.versionNumber})>"