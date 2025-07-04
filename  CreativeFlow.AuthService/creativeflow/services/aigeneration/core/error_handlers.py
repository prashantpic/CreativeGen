import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from ..application.services.credit_service_client import InsufficientCreditsError, CreditServiceError

logger = logging.getLogger(__name__)

class GenerationJobPublishError(Exception):
    """Custom exception for RabbitMQ publishing failures."""
    pass

class GenerationRequestNotFoundError(Exception):
    """Custom exception for when a generation request is not found."""
    pass
    
class InvalidGenerationStateError(Exception):
    """Custom exception for operations on a request in an invalid state."""
    pass


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handles Pydantic's RequestValidationError, returning a 422 response.
    """
    logger.warning(f"Validation error for request {request.method} {request.url}: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )

async def insufficient_credits_exception_handler(request: Request, exc: InsufficientCreditsError):
    """
    Handles InsufficientCreditsError, returning a 402 Payment Required response.
    """
    logger.warning(f"Insufficient credits for user: {exc}")
    return JSONResponse(
        status_code=status.HTTP_402_PAYMENT_REQUIRED,
        content={"detail": str(exc)},
    )

async def credit_service_exception_handler(request: Request, exc: CreditServiceError):
    """
    Handles general CreditServiceError, returning a 503 Service Unavailable response.
    """
    logger.error(f"Credit Service communication error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": f"Credit service is currently unavailable: {exc}"},
    )

async def generation_job_publish_exception_handler(request: Request, exc: GenerationJobPublishError):
    """
    Handles failures in publishing jobs to RabbitMQ, returning 500.
    """
    logger.critical(f"Failed to publish generation job to message queue: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Could not queue the generation job. Please try again later."},
    )
    
async def generation_request_not_found_handler(request: Request, exc: GenerationRequestNotFoundError):
    """
    Handles when a generation request is not found, returning 404.
    """
    logger.warning(f"Generation request not found: {exc}")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )
    
async def invalid_generation_state_handler(request: Request, exc: InvalidGenerationStateError):
    """
    Handles operations on requests in an invalid state, returning 409 Conflict.
    """
    logger.warning(f"Invalid operation for generation request state: {exc}")
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )

async def generic_exception_handler(request: Request, exc: Exception):
    """
    Handles any other unhandled exception, returning a generic 500 response.
    """
    logger.error(f"Unhandled exception for request {request.method} {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected internal server error occurred."},
    )

def add_exception_handlers(app):
    """
    Adds all custom exception handlers to the FastAPI application instance.
    """
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(InsufficientCreditsError, insufficient_credits_exception_handler)
    app.add_exception_handler(CreditServiceError, credit_service_exception_handler)
    app.add_exception_handler(GenerationJobPublishError, generation_job_publish_exception_handler)
    app.add_exception_handler(GenerationRequestNotFoundError, generation_request_not_found_handler)
    app.add_exception_handler(InvalidGenerationStateError, invalid_generation_state_handler)
    app.add_exception_handler(Exception, generic_exception_handler)