"""
This module defines custom exceptions for the application layer.
These exceptions are used to signal specific business logic or service-level errors,
allowing for standardized handling in the API layer.
"""

class ApplicationException(Exception):
    """Base class for custom application exceptions."""
    pass

class EntityNotFoundError(ApplicationException):
    """Raised when a requested entity (e.g., a generation request) is not found."""
    pass

class InsufficientCreditsError(ApplicationException):
    """Raised when a user does not have enough credits to perform an action."""
    pass

class CreditServiceError(ApplicationException):
    """Raised when there is an issue communicating with the Credit Service."""
    pass

class GenerationJobPublishError(ApplicationException):
    """Raised when a generation job cannot be published to the message queue."""
    pass

class InvalidStateTransitionError(ApplicationException):
    """Raised when an action is attempted on an entity in an invalid state."""
    pass