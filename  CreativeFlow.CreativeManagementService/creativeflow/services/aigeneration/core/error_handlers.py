import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from ..application.services.orchestration_service import (
    InsufficientCreditsError,
    GenerationJobPublishError,
    InvalidGenerationStateError
)

logger = logging.getLogger(__name__)

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
    logger.warning(f"Insufficient credits for user {exc.user_id}: {exc.detail}")
    return JSONResponse(
        status_code=status.HTTP_402_PAYMENT_REQUIRED,
        content={"detail": exc.detail},
    )

async def generation_job_publish_exception_handler(request: Request, exc: GenerationJobPublishError):
    """
    Handles GenerationJobPublishError, returning a 500 Internal Server Error response.
    """
    logger.error(f"Failed to publish generation job for request {exc.request_id}: {exc.detail}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Failed to publish generation job: {exc.detail}"},
    )

async def invalid_state_exception_handler(request: Request, exc: InvalidGenerationStateError):
    """
    Handles InvalidGenerationStateError, returning a 409 Conflict response.
    This occurs when an operation is attempted on a request in an invalid state.
    """
    logger.warning(f"Invalid state for operation on request {exc.request_id}. Current: {exc.current_status}, Expected: {exc.expected_status}. Detail: {exc.detail}")
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": exc.detail},
    )

async def generic_exception_handler(request: Request, exc: Exception):
    """
    Handles any other unhandled exception, returning a 500 response.
    """
    logger.error(f"Unhandled exception for request {request.method} {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected internal server error occurred."},
    )

def setup_error_handlers(app):
    """
    Registers all custom exception handlers with the FastAPI application.
    """
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(InsufficientCreditsError, insufficient_credits_exception_handler)
    app.add_exception_handler(GenerationJobPublishError, generation_job_publish_exception_handler)
    app.add_exception_handler(InvalidGenerationStateError, invalid_state_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)