```python
import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from creativeflow.services.aigeneration.application.exceptions import (
    ApplicationException,
    InsufficientCreditsError,
    GenerationRequestNotFound,
    InvalidGenerationStateError
)

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

async def application_exception_handler(request: Request, exc: ApplicationException):
    """
    Handles custom application-level exceptions and maps them to appropriate
    HTTP status codes and error responses.
    """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    
    if isinstance(exc, InsufficientCreditsError):
        status_code = status.HTTP_402_PAYMENT_REQUIRED
    elif isinstance(exc, GenerationRequestNotFound):
        status_code = status.HTTP_404_NOT_FOUND
    elif isinstance(exc, InvalidGenerationStateError):
        status_code = status.HTTP_409_CONFLICT
    
    logger.error(
        f"Application error for request {request.method} {request.url}: {exc.detail}",
        exc_info=True if status_code == 500 else False
    )
    
    return JSONResponse(
        status_code=status_code,
        content={"detail": exc.detail},
    )
```