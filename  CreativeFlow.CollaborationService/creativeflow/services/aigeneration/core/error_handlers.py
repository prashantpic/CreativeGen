import logging
from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from creativeflow.services.aigeneration.application.exceptions import (
    InsufficientCreditsError, GenerationJobPublishError, EntityNotFoundError,
    InvalidStateTransitionError, CreditServiceError
)

logger = logging.getLogger(__name__)

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handles Pydantic's RequestValidationError.
    Returns a 422 Unprocessable Entity response with a structured error detail.
    """
    logger.warning(
        "Request validation error for path: %s",
        request.url.path,
        extra={"errors": exc.errors()}
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )

async def entity_not_found_exception_handler(request: Request, exc: EntityNotFoundError):
    """
    Handles custom EntityNotFoundError.
    Returns a 404 Not Found response.
    """
    logger.warning("Entity not found at path %s: %s", request.url.path, exc)
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )

async def insufficient_credits_exception_handler(request: Request, exc: InsufficientCreditsError):
    """
    Handles custom InsufficientCreditsError.
    Returns a 402 Payment Required response.
    """
    logger.warning(
        "Insufficient credits for user at path %s: %s", request.url.path, exc
    )
    return JSONResponse(
        status_code=status.HTTP_402_PAYMENT_REQUIRED,
        content={"detail": str(exc)},
    )

async def invalid_state_transition_exception_handler(request: Request, exc: InvalidStateTransitionError):
    """
    Handles invalid state transition errors (e.g., selecting sample on a completed request).
    Returns a 409 Conflict response.
    """
    logger.warning(
        "Invalid state transition attempted at path %s: %s", request.url.path, exc
    )
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )

async def job_publish_exception_handler(request: Request, exc: GenerationJobPublishError):
    """
    Handles failures in publishing jobs to RabbitMQ.
    Returns a 503 Service Unavailable response.
    """
    logger.error(
        "Failed to publish generation job to message queue at path %s: %s",
        request.url.path,
        exc,
        exc_info=True
    )
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": "Failed to queue generation job. Please try again later."},
    )
    
async def credit_service_exception_handler(request: Request, exc: CreditServiceError):
    """
    Handles failures in communicating with the Credit Service.
    Returns a 503 Service Unavailable response.
    """
    logger.error(
        "Error communicating with Credit Service at path %s: %s",
        request.url.path,
        exc,
        exc_info=True
    )
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": "Could not connect to the Credit Service. Please try again later."},
    )

async def generic_exception_handler(request: Request, exc: Exception):
    """

    Handles any other unhandled exceptions.
    Returns a 500 Internal Server Error response.
    """
    logger.error(
        "An unhandled exception occurred for request %s: %s",
        request.url.path,
        exc,
        exc_info=True
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred."},
    )

def setup_error_handlers(app):
    """
    Adds all custom exception handlers to the FastAPI app instance.
    """
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(EntityNotFoundError, entity_not_found_exception_handler)
    app.add_exception_handler(InsufficientCreditsError, insufficient_credits_exception_handler)
    app.add_exception_handler(InvalidStateTransitionError, invalid_state_transition_exception_handler)
    app.add_exception_handler(GenerationJobPublishError, job_publish_exception_handler)
    app.add_exception_handler(CreditServiceError, credit_service_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)