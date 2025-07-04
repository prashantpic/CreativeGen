"""
Pydantic schemas for content publishing and scheduling API requests and responses.
"""
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class GeneratedAsset(BaseModel):
    """Schema representing a media asset to be published."""
    url: str  # Could be a MinIO path or a public URL
    asset_type: str = Field(..., pattern="^(image|video)$")
    mime_type: str
    platform_media_id: Optional[str] = None


class PublishRequest(BaseModel):
    """Request schema for publishing content immediately."""
    connection_id: UUID
    text_content: Optional[str] = None
    assets: List[GeneratedAsset] = Field(default_factory=list)
    platform_specific_options: Optional[Dict[str, Any]] = None

    @field_validator("assets")
    @classmethod
    def check_content_presence(cls, v, values):
        text_content = values.data.get('text_content')
        if not v and not text_content:
            raise ValueError("Either 'text_content' or 'assets' must be provided.")
        return v


class ScheduleRequest(PublishRequest):
    """Request schema for scheduling content for future publishing."""
    schedule_time: datetime

    @field_validator("schedule_time")
    @classmethod
    def schedule_time_must_be_in_future(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            raise ValueError("schedule_time must be timezone-aware.")
        if v <= datetime.now(v.tzinfo):
            raise ValueError("schedule_time must be in the future.")
        return v


class PublishJobResponse(BaseModel):
    """Response schema representing a publishing job."""
    job_id: UUID
    status: str
    platform: str
    user_id: str
    created_at: datetime
    scheduled_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    error_message: Optional[str] = None
    post_url: Optional[str] = None

    class Config:
        from_attributes = True
        # Pydantic v2 requires this to map job_id from domain model's id
        populate_by_name = True 
        alias_generator = lambda field_name: {"job_id": "id"}.get(field_name, field_name)