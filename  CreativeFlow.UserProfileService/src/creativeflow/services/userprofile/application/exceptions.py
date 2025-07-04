"""
Custom exceptions for the application layer of UserProfile service.

These exceptions are raised by application services to indicate failures
in processing use cases, such as a failure to update a profile or process
a data privacy request.
"""


class UserProfileApplicationError(Exception):
    """Base class for all application-layer exceptions."""
    pass


class ProfileUpdateFailedError(UserProfileApplicationError):
    """Raised when an attempt to update a user profile fails."""
    pass


class DataPrivacyRequestProcessingError(UserProfileApplicationError):
    """Raised when processing a data privacy request fails."""
    pass


class ConsentManagementError(UserProfileApplicationError):
    """Raised for errors during consent management operations."""
    pass