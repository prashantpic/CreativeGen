"""
Pydantic schemas for API usage and quota related responses.
"""
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class UsageSummaryDataPoint(BaseModel):
    """Represents usage data for a single endpoint."""
    endpoint: str = Field(..., description="The API endpoint that was called.")
    call_count: int = Field(..., description="The number of times the endpoint was called in the period.")
    cost: Optional[Decimal] = Field(None, description="The total cost associated with calls to this endpoint, if applicable.")


class UsageSummaryResponseSchema(BaseModel):
    """Schema for responding with an API usage summary."""
    api_client_id: UUID = Field(..., description="The ID of the API client (key) this summary is for.")
    user_id: UUID = Field(..., description="The ID of the user who owns the API client.")
    period_start: date = Field(..., description="The start date of the usage summary period.")
    period_end: date = Field(..., description="The end date of the usage summary period.")
    total_calls: int = Field(..., description="The total number of API calls made in the period.")
    total_cost: Optional[Decimal] = Field(None, description="The total cost of all API calls in the period, if applicable.")
    detailed_usage: List[UsageSummaryDataPoint] = Field(..., description="A breakdown of usage by endpoint.")
    
    class Config:
        from_attributes = True


class QuotaStatusResponseSchema(BaseModel):
    """Schema for responding with current quota status."""
    api_client_id: UUID = Field(..., description="The ID of the API client (key) this quota status is for.")
    user_id: UUID = Field(..., description="The ID of the user who owns the API client.")
    quota_type: str = Field(..., description="The type of quota being reported (e.g., 'generations').")
    limit: int = Field(..., description="The total quota limit for the period.")
    remaining: int = Field(..., description="The remaining number of units in the current quota period.")
    period: str = Field(..., description="The quota period (e.g., 'monthly', 'daily').")
    resets_at: Optional[datetime] = Field(None, description="The timestamp when the quota will reset.")

    class Config:
        from_attributes = True


class RateLimitStatusResponseSchema(BaseModel):
    """Schema for responding with rate limit status information."""
    allowed: bool = Field(..., description="Whether the request is allowed under the current rate limit.")
    remaining_requests: Optional[int] = Field(None, description="The number of requests remaining in the current window.")
    retry_after_seconds: Optional[int] = Field(None, description="The number of seconds to wait before the next request will be allowed.")