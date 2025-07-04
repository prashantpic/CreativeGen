"""
Domain models for handling data privacy requests and retention policies.
"""
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class DataPrivacyRequestType(str, Enum):
    """Enumeration of GDPR/CCPA data privacy request types."""
    ACCESS = "access"
    PORTABILITY = "portability"
    DELETION = "deletion"
    RECTIFICATION = "rectification"


class DataPrivacyRequestStatus(str, Enum):
    """Enumeration of the statuses for a data privacy request."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class RetentionRuleAction(str, Enum):
    """Enumeration of actions to take for a data retention rule."""
    DELETE = "delete"
    ANONYMIZE = "anonymize"


class DataPrivacyRequest(BaseModel):
    """
    Represents a user's data privacy request (e.g., GDPR, CCPA) as an Entity.

    Attributes:
        id: The unique identifier for the request.
        auth_user_id: The identifier of the user making the request.
        request_type: The type of data privacy request.
        status: The current processing status of the request.
        details: Optional details, e.g., for a rectification request.
        created_at: Timestamp of when the request was made.
        updated_at: Timestamp of the last status update.
        processed_at: Timestamp of when the request was completed or failed.
        response_data_path: A path/URL to exported data for access/portability.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    auth_user_id: str
    request_type: DataPrivacyRequestType
    status: DataPrivacyRequestStatus = DataPrivacyRequestStatus.PENDING
    details: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    processed_at: Optional[datetime] = None
    response_data_path: Optional[str] = None

    def mark_as_processing(self) -> None:
        """Marks the request as currently being processed."""
        self.status = DataPrivacyRequestStatus.PROCESSING
        self.updated_at = datetime.now(timezone.utc)

    def mark_as_completed(self, response_data_path: Optional[str] = None) -> None:
        """
        Marks the request as completed.

        Args:
            response_data_path: Optional path to the resulting data file.
        """
        now = datetime.now(timezone.utc)
        self.status = DataPrivacyRequestStatus.COMPLETED
        self.processed_at = now
        self.updated_at = now
        if response_data_path:
            self.response_data_path = response_data_path

    def mark_as_failed(self, reason: str) -> None:
        """
        Marks the request as failed.

        Args:
            reason: A description of why the request failed.
        """
        self.status = DataPrivacyRequestStatus.FAILED
        self.details = reason
        now = datetime.now(timezone.utc)
        self.processed_at = now
        self.updated_at = now


class RetentionRule(BaseModel):
    """
    Represents a data retention rule as a Value Object.

    Attributes:
        data_category: A descriptor for the type of data this rule applies to.
        retention_period_days: The number of days to retain the data.
        action: The action to take when the retention period is met.
        basis: The event or timestamp from which the retention period starts.
    """
    data_category: str
    retention_period_days: int
    action: RetentionRuleAction
    basis: str  # e.g., "last_activity", "consent_revoked_date"