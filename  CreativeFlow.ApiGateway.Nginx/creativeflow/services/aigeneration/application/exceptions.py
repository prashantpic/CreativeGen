```python
class ApplicationException(Exception):
    """Base exception class for the application layer."""
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(self.detail)

class InsufficientCreditsError(ApplicationException):
    """Raised when a user has insufficient credits for an action."""
    pass

class CreditServiceError(ApplicationException):
    """Raised for generic errors from the Credit Service."""
    pass
    
class NotificationServiceError(ApplicationException):
    """Raised for errors from the Notification Service."""
    pass

class OdooAdapterError(ApplicationException):
    """Raised for errors during Odoo RPC calls."""
    pass

class GenerationRequestNotFound(ApplicationException):
    """Raised when a generation request is not found in the repository."""
    pass

class InvalidGenerationStateError(ApplicationException):
    """Raised when an action is attempted on a request in an invalid state."""
    pass

class GenerationJobPublishError(ApplicationException):
    """Raised when publishing a job to RabbitMQ fails."""
    pass
```