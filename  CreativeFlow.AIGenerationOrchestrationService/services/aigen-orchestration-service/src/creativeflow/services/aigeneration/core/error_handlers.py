"""
error_handlers.py

Custom exception handlers for the FastAPI application.

This module defines custom exception handlers to convert application exceptions 
into standardized, structured JSON error responses for API consumers.
"""

import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

# A logger for this module
logger = logging.getLogger(__name__)

# --- Custom Application Exceptions ---

class AppException(Exception):
    """Base exception for the application."""
    def __init__(self, detail: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)

class InsufficientCreditsError(AppException):
    """Raised when a user has insufficient credits for an operation."""
    def __init__(self, detail: str = "Insufficient credits for the requested operation."):
        super().__init__(detail, status_code=status.HTTP_402_PAYMENT_REQUIRED)

class GenerationJobPublishError(AppException):
    """Raised when publishing a job to the message queue fails."""
    def __init__(self, detail: str = "Failed to publish generation job to the queue."):
        super().__init__(detail, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

class NotFoundError(AppException):
    """Raised when a resource is not found."""
    def __init__(self, detail: str = "The requested resource was not found."):
        super().__init__(detail, status_code=status.HTTP_404_NOT_FOUND)

class ForbiddenError(AppException):
    """Raised when a user is not authorized to perform an action."""
    def __init__(self, detail: str = "You do not have permission to perform this action."):
        super().__init__(detail, status_code=status.HTTP_403_FORBIDDEN)

class BusinessLogicError(AppException):
    """Raised for general business logic validation failures."""
    def __init__(self, detail: str = "A business logic error occurred."):
        super().__init__(detail, status_code=status.HTTP_409_CONFLICT)


# --- Exception Handlers ---

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handles Pydantic's RequestValidationError.
    Returns a 422 Unprocessable Entity response with a structured list of errors.
    """
    error_details = []
    for error in exc.errors():
        error_details.append(
            {
                "loc": [str(loc) for loc in error["loc"]],
                "msg": error["msg"],
                "type": error["type"],
            }
        )
    logger.warning(
        "Request validation failed: %s", error_details, 
        extra={"path": request.url.path, "method": request.method}
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": error_details},
    )

async def app_exception_handler(request: Request, exc: AppException):
    """
    Handles custom application exceptions derived from AppException.
    Returns a JSON response with the status code and detail from the exception.
    """
    logger.error(
        "Application exception caught: %s", exc.detail, 
        extra={"status_code": exc.status_code, "path": request.url.path, "method": request.method},
        exc_info=True
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

def add_exception_handlers(app):
    """Adds all custom exception handlers to the FastAPI app instance."""
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(AppException, app_exception_handler)
    # Add handlers for specific exceptions if they need different logic
    app.add_exception_handler(InsufficientCreditsError, app_exception_handler)
    app.add_exception_handler(GenerationJobPublishError, app_exception_handler)
    app.add_exception_handler(NotFoundError, app_exception_handler)
    app.add_exception_handler(ForbiddenError, app_exception_handler)
    app.add_exception_handler(BusinessLogicError, app_exception_handler)