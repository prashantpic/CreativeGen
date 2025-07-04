import uuid
from sqlalchemy import (
    Column, DateTime, String, ForeignKey, Text, CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.schema import UniqueConstraint

from ..db.base import Base


class SocialMediaConnection(Base):
    """
    Stores user's connected social media accounts and OAuth tokens.
    """
    __tablename__ = 'social_media_connections'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userId = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    platform = Column(String(20), nullable=False)
    externalUserId = Column(String(100), nullable=False)
    accessToken = Column(Text, nullable=False)
    refreshToken = Column(Text, nullable=True)
    expiresAt = Column(DateTime, nullable=True)
    createdAt = Column(DateTime, nullable=False, server_default=func.now())
    updatedAt = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="social_media_connections")

    __table_args__ = (
        UniqueConstraint('userId', 'platform', name='uq_socialconnection_user_platform'),
        CheckConstraint(platform.in_(['Instagram', 'Facebook', 'LinkedIn', 'Twitter', 'Pinterest', 'TikTok']), name='ck_social_media_connection_platform'),
    )

    def __repr__(self):
        return f"<SocialMediaConnection(id={self.id}, userId='{self.userId}', platform='{self.platform}')>"