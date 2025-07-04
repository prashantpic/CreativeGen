"""
Pydantic schemas for social media insights API requests and responses.
"""
from typing import List, Optional

from pydantic import BaseModel, Field


class HashtagRequest(BaseModel):
    """Request schema for getting trending hashtag suggestions."""
    keywords: List[str] = Field(..., min_length=1)
    industry: Optional[str] = None
    limit: int = Field(10, gt=0, le=50)


class HashtagSuggestion(BaseModel):
    """Schema for a single hashtag suggestion."""
    tag: str
    score: Optional[float] = None


class HashtagResponse(BaseModel):
    """Response schema containing a list of hashtag suggestions."""
    suggestions: List[HashtagSuggestion]


class BestTimeToPostSuggestion(BaseModel):
    """Schema for a single best-time-to-post suggestion."""
    day_of_week: int = Field(..., ge=0, le=6)  # 0=Monday, 6=Sunday
    hour_of_day: int = Field(..., ge=0, le=23)
    score: Optional[float] = None


class BestTimeToPostResponse(BaseModel):
    """Response schema for best times to post."""
    suggested_times: List[BestTimeToPostSuggestion]
    confidence: Optional[str] = Field(None, pattern="^(high|medium|low)$")