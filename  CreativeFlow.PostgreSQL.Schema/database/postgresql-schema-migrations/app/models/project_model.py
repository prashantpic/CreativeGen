import uuid
from sqlalchemy import (
    Column, DateTime, String, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..db.base import Base


class Project(Base):
    """
    Represents a creative project containing assets and generation requests.
    """
    __tablename__ = 'projects'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workbenchId = Column(UUID(as_uuid=True), ForeignKey('workbenches.id', ondelete='CASCADE'), nullable=False, index=True)
    userId = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    templateId = Column(UUID(as_uuid=True), ForeignKey('templates.id', ondelete='SET NULL'), nullable=True)
    brandKitId = Column(UUID(as_uuid=True), ForeignKey('brand_kits.id', ondelete='SET NULL'), nullable=True)
    name = Column(String(100), nullable=False)
    targetPlatform = Column(String(50), nullable=True)
    collaborationState = Column(JSONB, nullable=True)
    lastCollaboratedAt = Column(DateTime, nullable=True)
    createdAt = Column(DateTime, nullable=False, server_default=func.now())
    updatedAt = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), index=True)
    deletedAt = Column(DateTime, nullable=True, index=True)

    # Relationships
    workbench = relationship("Workbench", back_populates="projects")
    user = relationship("User", back_populates="projects")
    template = relationship("Template", back_populates="projects_using_template")
    brand_kit = relationship("BrandKit")
    assets = relationship("Asset", back_populates="project", cascade="all, delete-orphan")
    versions = relationship("AssetVersion", back_populates="project", cascade="all, delete-orphan")
    generation_requests = relationship("GenerationRequest", back_populates="project")

    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}')>"