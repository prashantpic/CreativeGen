"""
Domain value object or entity representing fetched platform insights
(e.g., hashtags, best times).
"""
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel


class HashtagSuggestionVO(BaseModel):
    """Value Object representing a single hashtag suggestion."""
    tag: str
    score: Optional[float] = None


class BestPostTimeVO(BaseModel):
    """Value Object representing a suggested time slot to post."""
    day_of_week: int  # 0-6, where Monday is 0
    hour_of_day: int  # 0-23
    score: Optional[float] = None


class InsightType(str, Enum):
    """Enumeration for the type of insight."""
    HASHTAGS = "hashtags"
    BEST_TIMES = "best_times"


class PlatformInsights(BaseModel):
    """
    Represents content optimization insights fetched from social media platforms.
    """
    platform: str
    insight_type: InsightType
    data: Union[List[HashtagSuggestionVO], List[BestPostTimeVO]]
    generated_at: datetime
    context_params: Optional[Dict[str, Any]] = None