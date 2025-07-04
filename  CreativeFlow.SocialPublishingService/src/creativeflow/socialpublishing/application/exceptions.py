"""
Custom exceptions for the application layer.

These exceptions provide more specific error information than generic exceptions
and can be caught by the API layer to return appropriate HTTP responses.
"""
from typing import Any


class SocialPublishingBaseError(Exception):
    """Base exception for all application-specific errors."""
    pass


class OAuthConnectionError(SocialPublishingBaseError):
    """Raised for errors during the OAuth connection process."""
    pass


class PublishingError(SocialPublishingBaseError):
    """Raised for general errors during content publishing."""
    pass


class InsufficientPermissionsError(SocialPublishingBaseError):
    """
    Raised when a user attempts an action for which they lack the necessary
    permissions from the social media platform.
    """
    pass


class PlatformApiError(SocialPublishingBaseError):
    """
    Raised when a social media platform's API returns an error.
    """
    def __init__(self, platform: str, status_code: int, details: Any, *args):
        self.platform = platform
        self.status_code = status_code
        self.details = details
        message = (
            f"Platform API error for {platform}. "
            f"Status: {status_code}, Details: {details}"
        )
        super().__init__(message, *args)


class RateLimitError(PlatformApiError):
    """Raised specifically when a platform's rate limit has been exceeded."""
    pass


class TokenEncryptionError(SocialPublishingBaseError):
    """Raised for errors during token encryption or decryption."""
    pass


class TokenExpiredError(SocialPublishingBaseError):
    """Raised when a token is expired and cannot be refreshed."""
    pass


class ContentValidationError(SocialPublishingBaseError):
    """Raised when content fails validation against platform policies."""
    pass


class JobNotFoundError(SocialPublishingBaseError):
    """Raised when a specific publishing job cannot be found."""
    pass

class ConnectionNotFoundError(SocialPublishingBaseError):
    """Raised when a specific social connection cannot be found."""
    pass

class PermissionDeniedError(SocialPublishingBaseError):
    """Raised when a user tries to access a resource they do not own."""
    pass