import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

logger = logging.getLogger(__name__)

# --- Custom Application Exceptions ---

class ApplicationException(Exception):
    """Base class for application-specific exceptions."""
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(self.detail)

class InsufficientCreditsError(ApplicationException):
    """Raised when a user has insufficient credits for an action."""
    pass

class GenerationJobPublishError(ApplicationException):
    """Raised when publishing a job to RabbitMQ fails."""
    pass
    
class InvalidGenerationStateError(ApplicationException):
    """Raised when an action is attempted on a generation request in an invalid state."""
    pass

class CreditServiceError(ApplicationException):
    """Raised when there's an issue communicating with the Credit Service."""
    pass

# --- Exception Handlers ---

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handles Pydantic's RequestValidationError.
    Returns a 422 Unprocessable Entity response with structured error details.
    """
    logger.warning(f"Validation error for request {request.method} {request.url}: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )

async def insufficient_credits_exception_handler(request: Request, exc: InsufficientCreditsError):
    """Handles InsufficientCreditsError and returns a 402 Payment Required."""
    logger.warning(f"Insufficient credits for request {request.method} {request.url}: {exc.detail}")
    return JSONResponse(
        status_code=status.HTTP_402_PAYMENT_REQUIRED,
        content={"detail": exc.detail},
    )

async def invalid_state_exception_handler(request: Request, exc: InvalidGenerationStateError):
    """Handles InvalidGenerationStateError and returns a 409 Conflict."""
    logger.warning(f"Invalid state for request {request.method} {request.url}: {exc.detail}")
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": exc.detail},
    )

async def generic_application_exception_handler(request: Request, exc: ApplicationException):
    """
    Handles generic ApplicationException and returns a 500 Internal Server Error.
    This can be used for errors like job publishing failures.
    """
    logger.error(
        f"Application error for request {request.method} {request.url}: {exc.detail}",
        exc_info=True
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": exc.detail},
    )

async def http_exception_handler(request: Request, exc: Exception):
    """
    Generic fallback handler for unhandled exceptions.
    Returns a 500 Internal Server Error.
    """
    logger.error(
        f"Unhandled exception for request {request.method} {request.url}",
        exc_info=True
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred."},
    )

def setup_error_handlers(app):
    """Adds all custom exception handlers to the FastAPI app."""
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(InsufficientCreditsError, insufficient_credits_exception_handler)
    app.add_exception_handler(InvalidGenerationStateError, invalid_state_exception_handler)
    app.add_exception_handler(ApplicationException, generic_application_exception_handler)
    app.add_exception_handler(Exception, http_exception_handler)
    logger.info("Custom error handlers have been set up.")