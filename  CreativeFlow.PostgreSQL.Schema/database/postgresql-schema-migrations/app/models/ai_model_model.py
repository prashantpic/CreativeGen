import uuid
from sqlalchemy import (
    Boolean, Column, DateTime, String, Text, CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..db.base import Base


class AIModel(Base):
    """
    Metadata for AI models available on the platform (internal or external).
    """
    __tablename__ = 'ai_models'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    provider = Column(String(50), nullable=False)
    taskType = Column(String(50), nullable=False, index=True)
    isActive = Column(Boolean, nullable=False, default=True, index=True)
    createdAt = Column(DateTime, nullable=False, server_default=func.now())
    updatedAt = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Relationships
    versions = relationship("AIModelVersion", back_populates="ai_model_parent", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint(taskType.in_([
            'ImageGeneration', 'TextGeneration', 'ImageTransformation', 
            'StyleTransfer', 'ContentSafety'
        ]), name='ck_ai_model_task_type'),
    )

    def __repr__(self):
        return f"<AIModel(id={self.id}, name='{self.name}')>"