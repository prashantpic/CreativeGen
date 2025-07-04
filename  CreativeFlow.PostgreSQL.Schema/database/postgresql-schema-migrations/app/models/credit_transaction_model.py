import uuid
from sqlalchemy import (
    Column, DateTime, String, ForeignKey, Text, DECIMAL
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..db.base import Base


class CreditTransaction(Base):
    """
    Logs credit purchases, refunds, and consumption for billing and auditing.
    """
    __tablename__ = 'credit_transactions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userId = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    odooInvoiceId = Column(String(255), nullable=True)
    generationRequestId = Column(UUID(as_uuid=True), ForeignKey('generation_requests.id', ondelete='SET NULL'), nullable=True, index=True)
    apiCallId = Column(String(255), nullable=True)
    amount = Column(DECIMAL(10, 2), nullable=False)
    actionType = Column(String(50), nullable=False, index=True)
    description = Column(Text, nullable=True)
    createdAt = Column(DateTime, nullable=False, server_default=func.now(), index=True)
    syncedAt = Column(DateTime, nullable=False, server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="credit_transactions")
    generation_request = relationship("GenerationRequest", back_populates="credit_transactions")

    def __repr__(self):
        return f"<CreditTransaction(id={self.id}, userId='{self.userId}', amount={self.amount})>"