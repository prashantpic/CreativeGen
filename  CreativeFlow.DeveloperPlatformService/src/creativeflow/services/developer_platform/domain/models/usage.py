"""
Domain models for API usage records, quotas, and related value objects.
"""
import enum
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class APIUsageRecord(BaseModel):
    """
    Entity representing a single, recorded API call. This serves as a log
    for billing, analytics, and quota tracking.
    """
    id: UUID = Field(default_factory=uuid4)
    api_client_id: UUID
    user_id: UUID
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    endpoint: str
    cost: Optional[Decimal] = Field(None, description="Cost in credits or currency, if applicable.")
    is_successful: bool

    class Config:
        from_attributes = True


class QuotaPeriod(str, enum.Enum):
    """Value Object for the time period of a quota."""
    DAILY = "daily"
    MONTHLY = "monthly"


class Quota(BaseModel):
    """

    Entity representing a usage quota for a specific API client.
    The current usage is not stored here but calculated on-demand from
    APIUsageRecord entities.
    """
    id: UUID = Field(default_factory=uuid4)
    api_client_id: UUID
    user_id: UUID
    limit_amount: int
    period: QuotaPeriod
    last_reset_at: datetime

    class Config:
        from_attributes = True