"""
Internal DTOs (Data Transfer Objects) for the application layer.

These Pydantic schemas define data structures for internal use within the
application layer, such as for data transfer between service methods or for
mapping from domain entities. They are distinct from API schemas to allow for
internal variations without exposing them directly to the public API contract.
"""
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from ..domain.models.consent import ConsentType
from ..domain.models.data_privacy import (DataPrivacyRequestStatus,
                                          DataPrivacyRequestType)


class PreferencesSchema(BaseModel):
    """DTO for user preferences."""
    language_preference: str
    timezone: str
    ui_settings: dict


class UserProfileSchema(BaseModel):
    """DTO for a user profile."""
    id: UUID
    auth_user_id: str
    full_name: Optional[str]
    username: Optional[str]
    profile_picture_url: Optional[str]
    preferences: PreferencesSchema
    created_at: datetime
    updated_at: datetime
    last_activity_at: datetime
    is_anonymized: bool

    class Config:
        from_attributes = True


class ConsentSchema(BaseModel):
    """DTO for a user consent record."""
    id: UUID
    auth_user_id: str
    consent_type: ConsentType
    is_granted: bool
    version: str
    timestamp: datetime

    class Config:
        from_attributes = True


class DataPrivacyRequestSchema(BaseModel):
    """DTO for a data privacy request."""
    id: UUID
    auth_user_id: str
    request_type: DataPrivacyRequestType
    status: DataPrivacyRequestStatus
    details: Optional[str]
    created_at: datetime
    updated_at: datetime
    processed_at: Optional[datetime]
    response_data_path: Optional[str]

    class Config:
        from_attributes = True


class UserProfileDataExportSchema(BaseModel):
    """
    DTO for the data package exported for a data access/portability request.
    """
    profile: UserProfileSchema
    consents: List[ConsentSchema]