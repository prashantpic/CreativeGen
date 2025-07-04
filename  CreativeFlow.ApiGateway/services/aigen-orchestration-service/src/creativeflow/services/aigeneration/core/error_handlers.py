import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from creativeflow.services.aigeneration.application.services.credit_service_client import InsufficientCreditsError, CreditServiceError
from creativeflow.services.aigeneration.infrastructure.messaging.rabbitmq_publisher import GenerationJobPublishError

logger = logging.getLogger(__name__)

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handles Pydantic's RequestValidationError.
    Returns a 422 Unprocessable Entity response with structured error details.
    """
    logger.warning(f"Validation error for request {request.method} {request.url}: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )

async def insufficient_credits_exception_handler(request: Request, exc: InsufficientCreditsError):
    """
    Handles custom InsufficientCreditsError.
    Returns a 402 Payment Required response.
    """
    logger.info(f"Insufficient credits for request {request.method} {request.url}. User: {exc.user_id}, Required: {exc.required_credits}")
    return JSONResponse(
        status_code=status.HTTP_402_PAYMENT_REQUIRED,
        content={"detail": str(exc)},
    )

async def credit_service_exception_handler(request: Request, exc: CreditServiceError):
    """
    Handles generic errors from the Credit Service.
    Returns a 503 Service Unavailable response.
    """
    logger.error(f"Credit Service error for request {request.method} {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": "The credit service is currently unavailable. Please try again later."},
    )
    
async def job_publish_exception_handler(request: Request, exc: GenerationJobPublishError):
    """
    Handles errors when publishing a job to RabbitMQ.
    Returns a 503 Service Unavailable response.
    """
    logger.critical(f"Failed to publish generation job for request {request.method} {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": "Could not queue the generation job. Please try again later."},
    )

async def http_exception_handler(request: Request, exc: Exception):
    """
    Generic fallback exception handler.
    Returns a 500 Internal Server Error response.
    """
    logger.exception(f"An unhandled exception occurred for request {request.method} {request.url}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred."},
    )

def register_error_handlers(app):
    """
    Registers all custom exception handlers with the FastAPI app.
    """
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(InsufficientCreditsError, insufficient_credits_exception_handler)
    app.add_exception_handler(CreditServiceError, credit_service_exception_handler)
    app.add_exception_handler(GenerationJobPublishError, job_publish_exception_handler)
    # A generic handler for any other Exception should be last
    app.add_exception_handler(Exception, http_exception_handler)