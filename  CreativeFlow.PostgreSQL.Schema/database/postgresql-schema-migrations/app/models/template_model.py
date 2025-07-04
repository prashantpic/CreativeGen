import uuid
from sqlalchemy import (
    Boolean, Column, DateTime, String, ForeignKey, Text
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..db.base import Base


class Template(Base):
    """
    Stores predefined system templates and user-saved private templates.
    """
    __tablename__ = 'templates'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userId = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=False, index=True)
    previewUrl = Column(String(1024), nullable=False)
    sourceData = Column(JSONB, nullable=False)
    tags = Column(JSONB, nullable=True)
    isPublic = Column(Boolean, nullable=False, default=True)
    createdAt = Column(DateTime, nullable=False, server_default=func.now())
    updatedAt = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Relationships
    user_creator = relationship("User", back_populates="created_templates")
    projects_using_template = relationship("Project", back_populates="template")

    def __repr__(self):
        return f"<Template(id={self.id}, name='{self.name}')>"