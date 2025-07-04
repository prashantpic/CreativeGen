"""
Custom exceptions for the user profile domain.

These exceptions provide specific error context for issues arising within
the domain layer, allowing for more precise error handling in the
application and API layers.
"""


class UserProfileDomainError(Exception):
    """Base class for all domain-specific exceptions."""
    pass


class ProfileNotFoundError(UserProfileDomainError):
    """Raised when a user profile is not found for a given identifier."""
    pass


class InvalidPreferenceError(UserProfileDomainError):
    """Raised when a user preference value is invalid."""
    pass


class ConsentNotFoundError(UserProfileDomainError):
    """Raised when a specific consent record is not found."""
    pass


class ConsentAlreadyExistsError(UserProfileDomainError):
    """Raised when attempting to create a consent that already exists."""
    pass


class DataPrivacyRequestError(UserProfileDomainError):
    """Raised for general errors related to data privacy requests."""
    pass