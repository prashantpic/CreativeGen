"""
This module contains Pydantic Data Transfer Objects (DTOs) related to
User Account and Profile Management. These models define the data contracts for
API requests and responses, ensuring type safety and validation.
"""
from typing import Optional

from pydantic import EmailStr, Field, field_validator

from ..validation.validators import validate_password_complexity
from .base import BaseDTO, BaseResponseDTO


# =============================================================================
# Request DTOs
# =============================================================================

class UserCreateDTO(BaseDTO):
    """DTO for creating a new user account."""
    email: EmailStr
    password: str = Field(
        ...,
        min_length=12,
        description="User password, must meet complexity requirements."
    )

    @field_validator('password', check_fields=False)
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Applies the shared password complexity validator."""
        return validate_password_complexity(v)


class UserLoginDTO(BaseDTO):
    """DTO for user login requests."""
    email: EmailStr
    password: str


class UserUpdateDTO(BaseDTO):
    """DTO for updating a user's profile information. All fields are optional."""
    full_name: Optional[str] = Field(None, max_length=100)
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    profile_picture_url: Optional[str] = Field(None, max_length=1024)
    language_preference: Optional[str] = Field(None, max_length=10)
    timezone: Optional[str] = Field(None, max_length=50)


# =============================================================================
# Response DTOs
# =============================================================================

class UserResponseDTO(BaseResponseDTO):
    """DTO for returning public user information."""
    email: EmailStr
    full_name: Optional[str]
    username: Optional[str]
    profile_picture_url: Optional[str]
    subscription_tier: str
    credit_balance: float
    is_email_verified: bool
    mfa_enabled: bool


class TokenResponseDTO(BaseDTO):
    """DTO for returning authentication tokens after a successful login."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"