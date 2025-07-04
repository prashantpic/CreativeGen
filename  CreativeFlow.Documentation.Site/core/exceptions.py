```python
from fastapi import HTTPException


class AppException(HTTPException):
    """Base custom exception for the application."""
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class APIKeyNotFoundError(AppException):
    """Raised when an API key is not found in the database."""
    def __init__(self, detail: str = "API Key not found."):
        super().__init__(status_code=404, detail=detail)


class APIKeyInactiveError(AppException):
    """Raised when an API key is inactive or revoked."""
    def __init__(self, detail: str = "API Key is inactive or has been revoked."):
        super().__init__(status_code=403, detail=detail)

class APIKeyInvalidError(AppException):
    """Raised when an API key is invalid (e.g., bad format or failed verification)."""
    def __init__(self, detail: str = "Invalid or malformed API Key."):
        super().__init__(status_code=401, detail=detail)


class APIKeyPermissionDeniedError(AppException):
    """Raised when an API key does not have sufficient permissions for an action."""
    def __init__(self, detail: str = "API Key does not have sufficient permissions."):
        super().__init__(status_code=403, detail=detail)


class WebhookNotFoundError(AppException):
    """Raised when a webhook configuration is not found."""
    def __init__(self, detail: str = "Webhook not found."):
        super().__init__(status_code=404, detail=detail)


class InsufficientQuotaError(AppException):
    """Raised when an API client has exceeded their usage quota."""
    def __init__(self, detail: str = "API quota exceeded. Please check your plan and billing details."):
        super().__init__(status_code=429, detail=detail)


class RateLimitExceededError(AppException):
    """Raised when an API client has exceeded their rate limit."""
    def __init__(self, detail: str = "Rate limit exceeded. Please try again later."):
        super().__init__(
            status_code=429,
            detail=detail,
            # headers={"Retry-After": "60"} # This can be set dynamically
        )


class InvalidUserInputError(AppException):
    """Raised for general invalid user input that is not caught by Pydantic validation."""
    def __init__(self, detail: str = "Invalid user input provided."):
        super().__init__(status_code=400, detail=detail)


class ExternalServiceError(AppException):
    """Raised when communication with a downstream service fails."""
    def __init__(self, detail: str = "Error communicating with a downstream service."):
        super().__init__(status_code=502, detail=detail)


class NotAuthenticatedError(AppException):
    """Raised when a user is not authenticated for a management endpoint."""
    def __init__(self, detail: str = "Not authenticated"):
        super().__init__(
            status_code=401,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

class ForbiddenError(AppException):
    """Raised when an authenticated user does not have permission for an action."""
    def __init__(self, detail: str = "You do not have permission to perform this action."):
        super().__init__(status_code=403, detail=detail)
```