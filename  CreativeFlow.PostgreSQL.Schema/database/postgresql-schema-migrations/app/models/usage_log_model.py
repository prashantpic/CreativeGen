from sqlalchemy import (
    Column, DateTime, String, ForeignKey, DECIMAL, BigInteger
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..db.base import Base


class UsageLog(Base):
    """
    Detailed log of billable or trackable user actions for analytics and auditing.
    """
    __tablename__ = 'usage_logs'

    id = Column(BigInteger, primary_key=True)
    userId = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='SET NULL'), nullable=False, index=True)
    generationRequestId = Column(UUID(as_uuid=True), ForeignKey('generation_requests.id', ondelete='SET NULL'), nullable=True, index=True)
    apiClientId = Column(UUID(as_uuid=True), ForeignKey('api_clients.id', ondelete='SET NULL'), nullable=True, index=True)
    actionType = Column(String(100), nullable=False, index=True)
    details = Column(JSONB, nullable=True)
    creditsCost = Column(DECIMAL(10, 2), nullable=True)
    timestamp = Column(DateTime, nullable=False, server_default=func.now(), index=True)

    # Relationships
    user = relationship("User", back_populates="usage_logs")
    generation_request = relationship("GenerationRequest", back_populates="usage_logs")
    api_client = relationship("APIClient", back_populates="usage_logs")

    def __repr__(self):
        return f"<UsageLog(id={self.id}, userId='{self.userId}', actionType='{self.actionType}')>"