import logging
from typing import Any, Dict

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_429_TOO_MANY_REQUESTS,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_502_BAD_GATEWAY,
)

logger = logging.getLogger(__name__)


class AppException(HTTPException):
    """Base custom exception for the application."""

    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: Dict[str, Any] | None = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class APIKeyNotFoundError(AppException):
    """Raised when an API Key is not found."""

    def __init__(self, detail: str = "API Key not found.") -> None:
        super().__init__(status_code=HTTP_404_NOT_FOUND, detail=detail)


class APIKeyInactiveError(AppException):
    """Raised when an API Key is inactive."""

    def __init__(self, detail: str = "API Key is inactive.") -> None:
        super().__init__(status_code=HTTP_403_FORBIDDEN, detail=detail)

class APIKeyInvalidError(AppException):
    """Raised when an API Key is invalid or fails verification."""
    def __init__(self, detail: str = "Invalid or inactive API Key.") -> None:
        super().__init__(status_code=HTTP_401_UNAUTHORIZED, detail=detail, headers={"WWW-Authenticate": "APIKey"})


class APIKeyPermissionDeniedError(AppException):
    """Raised when an API Key has insufficient permissions."""

    def __init__(
        self, detail: str = "API Key does not have sufficient permissions."
    ) -> None:
        super().__init__(status_code=HTTP_403_FORBIDDEN, detail=detail)


class WebhookNotFoundError(AppException):
    """Raised when a Webhook is not found."""

    def __init__(self, detail: str = "Webhook not found.") -> None:
        super().__init__(status_code=HTTP_404_NOT_FOUND, detail=detail)


class InsufficientQuotaError(AppException):
    """Raised when a client's API quota is exceeded."""

    def __init__(self, detail: str = "API quota exceeded.") -> None:
        super().__init__(status_code=HTTP_429_TOO_MANY_REQUESTS, detail=detail)


class RateLimitExceededError(AppException):
    """Raised when a client's rate limit is exceeded."""

    def __init__(
        self,
        detail: str = "Rate limit exceeded.",
        retry_after: int | None = None,
    ) -> None:
        headers = {"Retry-After": str(retry_after)} if retry_after else None
        super().__init__(
            status_code=HTTP_429_TOO_MANY_REQUESTS, detail=detail, headers=headers
        )


class InvalidUserInputError(AppException):
    """Raised for general invalid user input."""

    def __init__(self, detail: str = "Invalid user input.") -> None:
        super().__init__(status_code=HTTP_400_BAD_REQUEST, detail=detail)


class ExternalServiceError(AppException):
    """Raised when communication with an external service fails."""

    def __init__(
        self, detail: str = "Error communicating with an external service."
    ) -> None:
        super().__init__(status_code=HTTP_502_BAD_GATEWAY, detail=detail)


# Exception Handlers to be registered in main.py
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handles custom application exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers,
    )


async def sqlalchemy_exception_handler(
    request: Request, exc: SQLAlchemyError
) -> JSONResponse:
    """Handles database exceptions."""
    # Note: In production, do not expose detailed exception messages.
    logger.error(f"Database error on request {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal database error occurred."},
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handles any other unhandled exceptions."""
    logger.critical(
        f"Unhandled exception on request {request.url.path}: {exc}", exc_info=True
    )
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected internal server error occurred."},
    )