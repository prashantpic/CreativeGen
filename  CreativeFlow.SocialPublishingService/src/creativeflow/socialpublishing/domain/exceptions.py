"""
Custom exceptions for the domain layer.
"""

class DomainBaseError(Exception):
    """Base exception for domain layer errors."""
    pass


class InvalidSocialPlatformError(ValueError, DomainBaseError):
    """Raised when an unsupported or invalid social platform is specified."""
    pass


class TokenExpiredError(Exception, DomainBaseError):
    """Raised when an OAuth token is expired and cannot be refreshed."""
    pass


class ContentValidationError(ValueError, DomainBaseError):
    """Raised when content violates platform-specific policies."""
    pass


class JobStateTransitionError(Exception, DomainBaseError):
    """Raised when there is an invalid state transition attempt on a PublishJob."""
    pass


class EntityNotFoundError(Exception, DomainBaseError):
    """Raised when a domain entity cannot be found."""
    pass