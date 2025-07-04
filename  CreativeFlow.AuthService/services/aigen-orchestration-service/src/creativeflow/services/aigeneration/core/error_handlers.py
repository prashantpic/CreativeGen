import logging
from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from creativeflow.services.aigeneration.application.services.orchestration_service import InsufficientCreditsError, GenerationJobPublishError, GenerationRequestStateError

logger = logging.getLogger(__name__)

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handles Pydantic's RequestValidationError and returns a 422 Unprocessable Entity
    response with a structured error message.
    """
    logger.warning(f"Validation error for request {request.method} {request.url}: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )

async def insufficient_credits_exception_handler(request: Request, exc: InsufficientCreditsError):
    """
    Handles InsufficientCreditsError and returns a 402 Payment Required response.
    """
    logger.warning(f"Insufficient credits for user {exc.user_id} on request {request.method} {request.url}. Reason: {exc.detail}")
    return JSONResponse(
        status_code=status.HTTP_402_PAYMENT_REQUIRED,
        content={"detail": str(exc)},
    )

async def generation_job_publish_exception_handler(request: Request, exc: GenerationJobPublishError):
    """
    Handles GenerationJobPublishError and returns a 500 Internal Server Error response.
    This indicates a critical failure in communicating with the message queue.
    """
    logger.error(f"Failed to publish generation job for request {request.method} {request.url}. Reason: {exc.detail}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Failed to queue generation task: {exc.detail}"},
    )

async def generation_request_state_exception_handler(request: Request, exc: GenerationRequestStateError):
    """
    Handles GenerationRequestStateError and returns a 409 Conflict response.
    This indicates an operation was attempted on a request in an invalid state.
    """
    logger.warning(f"Invalid state operation for request {request.method} {request.url}. Reason: {exc.detail}")
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )


def add_exception_handlers(app):
    """
    Adds all custom exception handlers to the FastAPI application instance.
    """
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(InsufficientCreditsError, insufficient_credits_exception_handler)
    app.add_exception_handler(GenerationJobPublishError, generation_job_publish_exception_handler)
    app.add_exception_handler(GenerationRequestStateError, generation_request_state_exception_handler)