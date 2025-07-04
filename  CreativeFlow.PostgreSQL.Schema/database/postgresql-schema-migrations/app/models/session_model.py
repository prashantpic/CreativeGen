import uuid
from sqlalchemy import (
    Column, DateTime, String, ForeignKey, Text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..db.base import Base


class Session(Base):
    """
    Stores user authentication sessions for web and mobile.
    """
    __tablename__ = 'sessions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userId = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    deviceInfo = Column(String(255), nullable=False)
    ipAddress = Column(String(45), nullable=False)
    userAgent = Column(Text, nullable=True)
    lastActivity = Column(DateTime, nullable=False, server_default=func.now(), index=True)
    expiresAt = Column(DateTime, nullable=False, index=True)
    createdAt = Column(DateTime, nullable=False, server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="sessions")

    def __repr__(self):
        return f"<Session(id={self.id}, userId='{self.userId}')>"