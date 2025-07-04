import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from creativeflow.services.aigeneration.application.services.credit_service_client import InsufficientCreditsError, CreditServiceError

logger = logging.getLogger(__name__)

# --- Custom Application Exceptions ---

class ApplicationException(Exception):
    """Base class for application-specific exceptions."""
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(self.detail)

class GenerationRequestNotFound(ApplicationException):
    """Raised when a generation request is not found in the repository."""
    pass

class InvalidGenerationStateError(ApplicationException):
    """Raised when an operation is attempted on a request in an invalid state."""
    pass

class GenerationJobPublishError(ApplicationException):
    """Raised when publishing a job to RabbitMQ fails."""
    pass

# --- FastAPI Exception Handlers ---

async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handles Pydantic's RequestValidationError.
    Returns a 422 Unprocessable Entity response with structured error details.
    """
    error_details = exc.errors()
    logger.warning(f"Request validation error: {error_details}", extra={"path": request.url.path})
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": error_details},
    )

async def insufficient_credits_exception_handler(request: Request, exc: InsufficientCreditsError):
    """
    Handles InsufficientCreditsError and returns a 402 Payment Required.
    """
    logger.warning(f"Insufficient credits for request: {exc.detail}", extra={"path": request.url.path})
    return JSONResponse(
        status_code=status.HTTP_402_PAYMENT_REQUIRED,
        content={"detail": exc.detail},
    )

async def credit_service_exception_handler(request: Request, exc: CreditServiceError):
    """
    Handles general CreditServiceError and returns a 503 Service Unavailable.
    """
    logger.error(f"Credit Service communication error: {exc.detail}", exc_info=True, extra={"path": request.url.path})
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": f"Credit service is currently unavailable: {exc.detail}"},
    )
    
async def generation_request_not_found_handler(request: Request, exc: GenerationRequestNotFound):
    """
    Handles GenerationRequestNotFound and returns a 404 Not Found.
    """
    logger.info(f"Generation request not found: {exc.detail}", extra={"path": request.url.path})
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.detail},
    )

async def invalid_generation_state_handler(request: Request, exc: InvalidGenerationStateError):
    """
    Handles InvalidGenerationStateError and returns a 409 Conflict.
    """
    logger.warning(f"Invalid generation state for operation: {exc.detail}", extra={"path": request.url.path})
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": exc.detail},
    )

async def generation_job_publish_error_handler(request: Request, exc: GenerationJobPublishError):
    """
    Handles GenerationJobPublishError and returns a 500 Internal Server Error.
    """
    logger.critical(f"Failed to publish generation job to message queue: {exc.detail}", exc_info=True, extra={"path": request.url.path})
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Could not queue generation job. Please try again later. Error: {exc.detail}"},
    )

async def generic_exception_handler(request: Request, exc: Exception):
    """
    Handles any other unhandled exception and returns a 500 Internal Server Error.
    """
    logger.exception(f"An unhandled exception occurred: {exc}", extra={"path": request.url.path})
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred."},
    )

def register_error_handlers(app):
    """
    Registers all custom exception handlers with the FastAPI application.
    """
    app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
    app.add_exception_handler(InsufficientCreditsError, insufficient_credits_exception_handler)
    app.add_exception_handler(CreditServiceError, credit_service_exception_handler)
    app.add_exception_handler(GenerationRequestNotFound, generation_request_not_found_handler)
    app.add_exception_handler(InvalidGenerationStateError, invalid_generation_state_handler)
    app.add_exception_handler(GenerationJobPublishError, generation_job_publish_error_handler)
    # The generic handler should be last
    app.add_exception_handler(Exception, generic_exception_handler)