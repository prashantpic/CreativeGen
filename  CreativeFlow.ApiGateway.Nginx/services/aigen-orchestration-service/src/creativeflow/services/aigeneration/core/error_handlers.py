import logging
from typing import Union

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# --- Custom Application Exceptions ---

class ApplicationException(Exception):
    """Base exception for the application."""
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(self.detail)

class InsufficientCreditsError(ApplicationException):
    """Raised when user has insufficient credits for an action."""
    pass

class GenerationJobPublishError(ApplicationException):
    """Raised when publishing a job to RabbitMQ fails."""
    pass
    
class ResourceNotFoundError(ApplicationException):
    """Raised when a requested resource is not found in the database."""
    pass

class InvalidStateError(ApplicationException):
    """Raised when an operation is attempted on a resource in an invalid state."""
    pass

class CreditDeductionError(ApplicationException):
    """Raised when credit deduction fails for a recoverable reason."""
    pass

# --- FastAPI Exception Handlers ---

class ErrorMessage(BaseModel):
    detail: Union[str, list]

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handles Pydantic's RequestValidationError.
    Returns a 422 Unprocessable Entity response with a structured error message.
    """
    error_details = exc.errors()
    logger.warning(f"Validation error for request {request.method} {request.url.path}: {error_details}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": error_details},
    )

async def resource_not_found_exception_handler(request: Request, exc: ResourceNotFoundError):
    logger.warning(f"Resource not found for request {request.method} {request.url.path}: {exc.detail}")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.detail},
    )

async def insufficient_credits_exception_handler(request: Request, exc: InsufficientCreditsError):
    logger.warning(f"Insufficient credits for user on request {request.method} {request.url.path}: {exc.detail}")
    return JSONResponse(
        status_code=status.HTTP_402_PAYMENT_REQUIRED,
        content={"detail": exc.detail},
    )
    
async def invalid_state_exception_handler(request: Request, exc: InvalidStateError):
    logger.warning(f"Invalid state for operation on request {request.method} {request.url.path}: {exc.detail}")
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": exc.detail},
    )

async def http_exception_handler(request: Request, exc: Exception):
    """

    Generic handler for unhandled exceptions.
    Returns a 500 Internal Server Error to prevent leaking implementation details.
    """
    logger.exception(
        f"Unhandled exception for request {request.method} {request.url.path}",
        exc_info=exc
    )
    
    # Custom Application Exceptions that should result in a 500
    if isinstance(exc, (GenerationJobPublishError, CreditDeductionError)):
         return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": exc.detail}
        )
        
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected internal server error occurred."},
    )