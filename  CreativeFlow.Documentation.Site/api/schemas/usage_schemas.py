```python
import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field


class UsageSummaryDataPoint(BaseModel):
    """Represents usage for a single endpoint."""
    endpoint: str
    call_count: int
    cost: Optional[Decimal] = Field(None, description="Aggregated cost for this endpoint, if applicable.")


class UsageSummaryResponseSchema(BaseModel):
    """Schema for the API usage summary response."""
    api_client_id: uuid.UUID
    period_start: date
    period_end: date
    total_calls: int
    total_cost: Optional[Decimal] = Field(None, description="Total aggregated cost for the period, if applicable.")
    detailed_usage: List[UsageSummaryDataPoint]

    model_config = {
        "from_attributes": True
    }


class QuotaStatusResponseSchema(BaseModel):
    """Schema for the current quota status response."""
    api_client_id: uuid.UUID
    user_id: uuid.UUID
    quota_type: str = Field(..., description="The type of quota being reported (e.g., 'generations').")
    limit: int = Field(..., description="The total quota limit for the period.")
    remaining: int = Field(..., description="The remaining quota for the current period.")
    period: str = Field(..., description="The quota period (e.g., 'monthly', 'daily').")
    resets_at: Optional[datetime] = Field(None, description="The timestamp when the quota will reset.")

    model_config = {
        "from_attributes": True
    }


class RateLimitStatusResponseSchema(BaseModel):
    """Schema for representing rate limit status (conceptual)."""
    allowed: bool
    remaining_requests: Optional[int] = None
    retry_after_seconds: Optional[int] = None
```