class ApplicationException(Exception):
    """Base exception for the application layer."""
    pass

class InsufficientCreditsError(ApplicationException):
    """Raised when a user has insufficient credits for an action."""
    pass

class CreditServiceError(ApplicationException):
    """Raised when there is an issue communicating with the Credit Service."""
    pass

class GenerationJobPublishError(ApplicationException):
    """Raised when there is an error publishing a job to the message queue."""
    pass

class ResourceNotFoundError(ApplicationException):
    """Raised when a requested resource (e.g., GenerationRequest) is not found."""
    pass

class InvalidStateError(ApplicationException):
    """Raised when an action is attempted on a resource in an invalid state."""
    pass

class OdooAdapterError(ApplicationException):
    """Raised for errors related to the Odoo Adapter Client."""
    pass