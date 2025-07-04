import uuid
from sqlalchemy import (
    Column, DateTime, String, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..db.base import Base


class Workbench(Base):
    """
    A container for organizing creative projects, belonging to a user.
    """
    __tablename__ = 'workbenches'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userId = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    defaultBrandKitId = Column(UUID(as_uuid=True), ForeignKey('brand_kits.id', ondelete='SET NULL'), nullable=True)
    createdAt = Column(DateTime, nullable=False, server_default=func.now())
    updatedAt = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="workbenches")
    default_brand_kit = relationship("BrandKit")
    projects = relationship("Project", back_populates="workbench", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Workbench(id={self.id}, name='{self.name}')>"