"""
Domain entity representing a content publishing or scheduling job.
"""
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class PublishJobStatus(str, Enum):
    """
    Enumeration for the status of a publishing job.
    """
    PENDING = "Pending"
    PROCESSING = "Processing"
    PUBLISHED = "Published"
    SCHEDULED = "Scheduled"
    FAILED = "Failed"
    CONTENT_REJECTED = "ContentRejected"


class PublishJob(BaseModel):
    """
    Represents a job to publish or schedule content, tracking its state and details.
    """
    id: UUID
    user_id: str
    social_connection_id: UUID
    platform: str
    content_text: Optional[str] = None
    asset_urls: List[str] = Field(default_factory=list)
    platform_specific_options: Optional[Dict[str, Any]] = None
    status: PublishJobStatus = PublishJobStatus.PENDING
    scheduled_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    error_message: Optional[str] = None
    attempts: int = 0
    post_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    def mark_as_processing(self) -> None:
        """Sets the job status to Processing."""
        self.status = PublishJobStatus.PROCESSING
        self.updated_at = datetime.now(timezone.utc)

    def mark_as_published(self, post_url: str) -> None:
        """Sets the job status to Published and records the post URL."""
        self.status = PublishJobStatus.PUBLISHED
        self.post_url = post_url
        self.published_at = datetime.now(timezone.utc)
        self.error_message = None
        self.updated_at = datetime.now(timezone.utc)

    def mark_as_failed(self, error: str) -> None:
        """Sets the job status to Failed and records the error message."""
        self.status = PublishJobStatus.FAILED
        self.error_message = error
        self.updated_at = datetime.now(timezone.utc)

    def mark_as_content_rejected(self, reason: str) -> None:
        """Sets the job status to ContentRejected and records the reason."""
        self.status = PublishJobStatus.CONTENT_REJECTED
        self.error_message = reason
        self.updated_at = datetime.now(timezone.utc)

    def increment_attempts(self) -> None:
        """Increments the attempt counter for the job."""
        self.attempts += 1
        self.updated_at = datetime.now(timezone.utc)

    class Config:
        from_attributes = True