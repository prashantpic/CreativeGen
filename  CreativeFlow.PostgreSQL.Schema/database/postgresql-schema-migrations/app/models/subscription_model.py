import uuid
from sqlalchemy import (
    Column, DateTime, String, ForeignKey, CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..db.base import Base


class Subscription(Base):
    """
    Stores user subscription details, typically synced from Odoo.
    """
    __tablename__ = 'subscriptions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userId = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True, index=True)
    odooSaleOrderId = Column(String(255), unique=True, nullable=False, index=True)
    planId = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False, default='Active', index=True)
    currentPeriodStart = Column(DateTime, nullable=False)
    currentPeriodEnd = Column(DateTime, nullable=False, index=True)
    paymentProvider = Column(String(50), nullable=False)
    paymentProviderSubscriptionId = Column(String(255), nullable=True)
    paymentMethodId = Column(String(255), nullable=True)
    createdAt = Column(DateTime, nullable=False, server_default=func.now())
    updatedAt = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="subscription")

    __table_args__ = (
        CheckConstraint(status.in_(['Active', 'Trial', 'Suspended', 'Cancelled', 'Expired']), name='ck_subscription_status'),
        CheckConstraint(paymentProvider.in_(['Stripe', 'PayPal', 'OdooManual']), name='ck_subscription_payment_provider'),
    )

    def __repr__(self):
        return f"<Subscription(id={self.id}, userId='{self.userId}', planId='{self.planId}')>"