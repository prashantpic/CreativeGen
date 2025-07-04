```python
import uuid
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class APIUsageRecord(BaseModel):
    """Domain model for a single API usage record."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    api_client_id: uuid.UUID
    user_id: uuid.UUID
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    endpoint: str
    cost: Optional[Decimal] = None
    is_successful: bool
    
    class Config:
        from_attributes = True


class QuotaPeriod(str, Enum):
    """Value object for quota reset periods."""
    DAILY = "daily"
    MONTHLY = "monthly"


class Quota(BaseModel):
    """Domain model for a Quota entity."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    api_client_id: uuid.UUID
    user_id: uuid.UUID
    limit_amount: int
    period: QuotaPeriod
    last_reset_at: datetime

    class Config:
        from_attributes = True


# --- DTOs for Service layer ---

class UsageSummaryDataPoint(BaseModel):
    """Data point for usage summary."""
    endpoint: str
    call_count: int
    cost: Optional[Decimal] = None
    
class UsageSummary(BaseModel):
    """DTO representing an API usage summary."""
    api_client_id: uuid.UUID
    user_id: uuid.UUID
    period_start: date
    period_end: date
    total_calls: int = 0
    total_cost: Optional[Decimal] = Decimal("0.0")
    detailed_usage: List[UsageSummaryDataPoint] = []

    class Config:
        from_attributes = True


class QuotaStatus(BaseModel):
    """DTO representing the current quota status."""
    api_client_id: uuid.UUID
    user_id: uuid.UUID
    quota_type: str
    limit: int
    remaining: int
    period: str
    resets_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
```