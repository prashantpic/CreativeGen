"""
Domain model for user profile attributes and preferences.
"""
import uuid
from datetime import datetime, timezone
from typing import Dict, Optional

from pydantic import BaseModel, Field, HttpUrl


class Preferences(BaseModel):
    """
    Represents user-specific preferences as a Value Object.

    Attributes:
        language_preference: The user's preferred language (e.g., "en-US").
        timezone: The user's preferred timezone (e.g., "UTC", "America/New_York").
        ui_settings: A dictionary for storing various UI-related settings.
    """
    language_preference: str = Field(default="en-US", max_length=10)
    timezone: str = Field(default="UTC", max_length=50)
    ui_settings: Dict = Field(default_factory=dict)


class UserProfile(BaseModel):
    """
    Represents a user's profile as a domain Entity.

    This model encapsulates all data related to a user's profile, including
    personal details, preferences, and metadata for system operations like
    data retention. It also contains business logic for state transitions.

    Attributes:
        id: The unique identifier for the profile entity.
        auth_user_id: The identifier from the external authentication service.
        full_name: The user's full name.
        username: The user's chosen username.
        profile_picture_url: A URL pointing to the user's profile picture.
        preferences: A nested object containing user preferences.
        created_at: Timestamp of when the profile was created.
        updated_at: Timestamp of the last update to the profile.
        last_activity_at: Timestamp of the user's last recorded activity.
        is_anonymized: Flag indicating if the profile's PII has been anonymized.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    auth_user_id: str = Field(..., description="Identifier from Auth service, unique")
    full_name: Optional[str] = Field(None, max_length=100)
    username: Optional[str] = Field(
        None, max_length=50, pattern=r"^[a-zA-Z0-9_.-]+$"
    )
    profile_picture_url: Optional[HttpUrl] = None
    preferences: Preferences = Field(default_factory=Preferences)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_activity_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_anonymized: bool = False

    def update_details(
        self,
        full_name: Optional[str] = None,
        username: Optional[str] = None,
        profile_picture_url: Optional[HttpUrl] = None,
    ) -> None:
        """Updates profile detail fields if new values are provided."""
        if full_name is not None:
            self.full_name = full_name
        if username is not None:
            self.username = username
        if profile_picture_url is not None:
            self.profile_picture_url = profile_picture_url
        self.updated_at = datetime.now(timezone.utc)

    def update_preferences(
        self,
        language_preference: Optional[str] = None,
        timezone: Optional[str] = None,
        ui_settings: Optional[dict] = None,
    ) -> None:
        """Updates preference fields and sets the profile's updated_at."""
        if language_preference is not None:
            self.preferences.language_preference = language_preference
        if timezone is not None:
            self.preferences.timezone = timezone
        if ui_settings is not None:
            self.preferences.ui_settings = ui_settings
        self.updated_at = datetime.now(timezone.utc)

    def anonymize(self) -> None:
        """
        Anonymizes Personally Identifiable Information (PII) in the profile.
        Sets PII fields to placeholder values and marks the profile as anonymized.
        """
        self.full_name = "ANONYMIZED_USER"
        self.username = f"anonymized_{self.id}"
        self.profile_picture_url = None
        # Potentially anonymize parts of preferences if they contain PII
        # self.preferences.ui_settings = {}
        self.is_anonymized = True
        self.updated_at = datetime.now(timezone.utc)

    def record_activity(self) -> None:
        """Updates the last_activity_at timestamp to the current time."""
        now = datetime.now(timezone.utc)
        self.last_activity_at = now
        self.updated_at = now