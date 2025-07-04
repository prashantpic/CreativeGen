"""
Custom application-level exceptions.
"""

class ApplicationException(Exception):
    """Base class for application-specific exceptions."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class ResourceNotFoundError(ApplicationException):
    """Raised when a requested resource is not found."""
    pass

class InsufficientCreditsError(ApplicationException):
    """Raised when a user has insufficient credits for an action."""
    pass

class CreditServiceError(ApplicationException):
    """Raised when there is an error communicating with the credit service."""
    pass

class GenerationJobPublishError(ApplicationException):
    """Raised when a generation job fails to be published to the message queue."""
    pass

class InvalidGenerationStateError(ApplicationException):
    """Raised when an action is attempted on a generation request in an invalid state."""
    pass