import uuid
from sqlalchemy import (
    Boolean, Column, DateTime, String, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..db.base import Base


class BrandKit(Base):
    """
    Stores brand assets (colors, fonts, logos) and preferences
    for users or teams.
    """
    __tablename__ = 'brand_kits'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userId = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    teamId = Column(UUID(as_uuid=True), ForeignKey('teams.id', ondelete='CASCADE'), nullable=True, index=True)
    name = Column(String(100), nullable=False)
    colors = Column(JSONB, nullable=False, server_default='[]')
    fonts = Column(JSONB, nullable=False, server_default='[]')
    logos = Column(JSONB, nullable=True)
    stylePreferences = Column(JSONB, nullable=True)
    isDefault = Column(Boolean, nullable=False, default=False)
    createdAt = Column(DateTime, nullable=False, server_default=func.now())
    updatedAt = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="brand_kits")
    team = relationship("Team", back_populates="brand_kits")

    def __repr__(self):
        return f"<BrandKit(id={self.id}, name='{self.name}', userId='{self.userId}')>"