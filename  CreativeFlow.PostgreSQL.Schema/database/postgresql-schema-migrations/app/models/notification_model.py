import uuid
from sqlalchemy import (
    Boolean, Column, DateTime, String, ForeignKey, Text
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..db.base import Base


class Notification(Base):
    """
    Stores system-generated notifications for users.
    """
    __tablename__ = 'notifications'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userId = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    type = Column(String(50), nullable=False)
    message = Column(Text, nullable=False)
    metadata = Column(JSONB, nullable=True)
    isRead = Column(Boolean, nullable=False, default=False, index=True)
    createdAt = Column(DateTime, nullable=False, server_default=func.now(), index=True)
    updatedAt = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<Notification(id={self.id}, userId='{self.userId}', type='{self.type}')>"