"""
Domain model for user consents related to data processing.
"""
import uuid
from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


class ConsentType(str, Enum):
    """Enumeration of the types of consent a user can provide."""
    MARKETING_EMAILS = "marketing_emails"
    DATA_ANALYTICS = "data_analytics"
    BETA_PROGRAM = "beta_program"


class Consent(BaseModel):
    """
    Represents a user's consent for a specific data processing activity.

    This entity tracks the state of a user's consent, including what they
    consented to (type), whether it's granted, the version of the policy
    they agreed to, and when the consent state was last changed.

    Attributes:
        id: The unique identifier for the consent record.
        auth_user_id: The identifier of the user providing consent.
        consent_type: The category of data processing consent.
        is_granted: Boolean indicating if consent is currently granted.
        version: The version of the policy or terms consented to.
        timestamp: The timestamp of the last consent state change.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    auth_user_id: str
    consent_type: ConsentType
    is_granted: bool = False
    version: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def grant(self, version: str) -> None:
        """
        Grants consent for a specific version of a policy.

        Args:
            version: The version string of the policy being consented to.
        """
        self.is_granted = True
        self.version = version
        self.timestamp = datetime.now(timezone.utc)

    def withdraw(self) -> None:
        """
        Withdraws consent.
        """
        self.is_granted = False
        self.timestamp = datetime.now(timezone.utc)