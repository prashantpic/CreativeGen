import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from creativeflow.services.aigeneration.application.exceptions import (
    InsufficientCreditsError,
    CreditServiceError,
    GenerationJobPublishError,
    ResourceNotFoundError,
    InvalidStateError,
)

logger = logging.getLogger(__name__)

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handles Pydantic's RequestValidationError.
    Returns a 422 Unprocessable Entity response with structured error details.
    """
    logger.warning(f"Validation error for request {request.method} {request.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )

async def resource_not_found_exception_handler(request: Request, exc: ResourceNotFoundError):
    """
    Handles custom ResourceNotFoundError.
    Returns a 404 Not Found response.
    """
    logger.warning(f"Resource not found for request {request.method} {request.url.path}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )

async def insufficient_credits_exception_handler(request: Request, exc: InsufficientCreditsError):
    """
    Handles custom InsufficientCreditsError.
    Returns a 402 Payment Required response.
    """
    logger.warning(f"Insufficient credits for user action on {request.method} {request.url.path}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_402_PAYMENT_REQUIRED,
        content={"detail": str(exc)},
    )

async def credit_service_exception_handler(request: Request, exc: CreditServiceError):
    """
    Handles errors from the Credit Service client.
    Returns a 503 Service Unavailable response.
    """
    logger.error(f"Credit Service error for request {request.method} {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": f"Credit service unavailable: {exc}"},
    )

async def job_publish_exception_handler(request: Request, exc: GenerationJobPublishError):
    """
    Handles errors when publishing a job to RabbitMQ.
    Returns a 500 Internal Server Error response.
    """
    logger.critical(f"Failed to publish generation job for request {request.method} {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Failed to dispatch generation job: {exc}"},
    )

async def invalid_state_exception_handler(request: Request, exc: InvalidStateError):
    """
    Handles actions attempted on an entity in an invalid state.
    Returns a 409 Conflict response.
    """
    logger.warning(f"Invalid state for action on {request.method} {request.url.path}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )

async def generic_exception_handler(request: Request, exc: Exception):
    """
    Handles any other unhandled exceptions.
    Returns a 500 Internal Server Error response.
    """
    logger.error(f"Unhandled exception for request {request.method} {request.url.path}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected internal server error occurred."},
    )

def add_exception_handlers(app):
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(ResourceNotFoundError, resource_not_found_exception_handler)
    app.add_exception_handler(InsufficientCreditsError, insufficient_credits_exception_handler)
    app.add_exception_handler(CreditServiceError, credit_service_exception_handler)
    app.add_exception_handler(GenerationJobPublishError, job_publish_exception_handler)
    app.add_exception_handler(InvalidStateError, invalid_state_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)