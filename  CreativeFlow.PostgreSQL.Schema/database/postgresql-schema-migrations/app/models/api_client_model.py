import uuid
from sqlalchemy import (
    Boolean, Column, DateTime, String, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..db.base import Base


class APIClient(Base):
    """
    Stores API access credentials (keys and hashed secrets) for developers/API users.
    """
    __tablename__ = 'api_clients'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userId = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    apiKey = Column(String(100), unique=True, nullable=False, index=True)
    secretHash = Column(String(255), nullable=False)
    permissions = Column(JSONB, nullable=True)
    isActive = Column(Boolean, nullable=False, default=True)
    createdAt = Column(DateTime, nullable=False, server_default=func.now())
    updatedAt = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="api_clients")
    usage_logs = relationship("UsageLog", back_populates="api_client")

    def __repr__(self):
        return f"<APIClient(id={self.id}, name='{self.name}', userId='{self.userId}')>"