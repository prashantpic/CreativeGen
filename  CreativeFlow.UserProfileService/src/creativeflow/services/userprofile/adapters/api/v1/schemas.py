"""
Pydantic schemas for API request/response validation and serialization.

These models define the public contract of the API, ensuring that incoming
data is valid and outgoing data conforms to the expected structure.
"""
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl


# --- Preferences Schemas ---
class PreferencesResponseSchema(BaseModel):
    """API response schema for user preferences."""
    language_preference: str
    timezone: str
    ui_settings: Dict


# --- User Profile Schemas ---
class UserProfilePatchRequestSchema(BaseModel):
    """
    API request schema for partially updating a user profile.
    All fields are optional to support progressive profiling.
    """
    full_name: Optional[str] = Field(None, description="User's full name", max_length=100)
    username: Optional[str] = Field(
        None, description="User's chosen username", max_length=50, pattern=r"^[a-zA-Z0-9_.-]+$"
    )
    profile_picture_url: Optional[HttpUrl] = Field(None, description="URL to profile picture")
    language_preference: Optional[str] = Field(None, description="Preferred UI language (e.g., en-US)", max_length=10)
    timezone: Optional[str] = Field(None, description="User's preferred timezone (e.g., America/New_York)", max_length=50)
    ui_settings: Optional[Dict] = Field(None, description="JSON object for UI settings")


class UserProfileResponseSchema(BaseModel):
    """API response schema for a user profile."""
    auth_user_id: str
    full_name: Optional[str]
    username: Optional[str]
    profile_picture_url: Optional[HttpUrl]
    preferences: PreferencesResponseSchema
    created_at: datetime
    updated_at: datetime


class InitialProfileDataSchema(BaseModel):
    """API request schema for creating a profile with initial data."""
    language_preference: Optional[str] = Field(None, max_length=10)
    timezone: Optional[str] = Field(None, max_length=50)


# --- Consent Schemas ---
class ConsentTypeEnum(str, Enum):
    """API enum for consent types."""
    MARKETING_EMAILS = "marketing_emails"
    DATA_ANALYTICS = "data_analytics"
    BETA_PROGRAM = "beta_program"


class ConsentUpdateRequestSchema(BaseModel):
    """API request schema for updating a user's consent."""
    is_granted: bool
    version: str = Field(..., description="Version of the policy being consented to")


class ConsentResponseSchema(BaseModel):
    """API response schema for a user consent record."""
    consent_type: ConsentTypeEnum
    is_granted: bool
    version: str
    timestamp: datetime


# --- Data Privacy Schemas ---
class DataPrivacyRequestTypeEnum(str, Enum):
    """API enum for data privacy request types."""
    ACCESS = "access"
    PORTABILITY = "portability"
    DELETION = "deletion"
    RECTIFICATION = "rectification"


class DataPrivacyRequestStatusEnum(str, Enum):
    """API enum for data privacy request statuses."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class DataPrivacyRequestResponseSchema(BaseModel):
    """API response schema for a data privacy request."""
    id: UUID
    auth_user_id: str
    request_type: DataPrivacyRequestTypeEnum
    status: DataPrivacyRequestStatusEnum
    details: Optional[str]
    created_at: datetime
    processed_at: Optional[datetime]
    response_data_url: Optional[HttpUrl] = Field(None, description="Link to exported data if applicable")