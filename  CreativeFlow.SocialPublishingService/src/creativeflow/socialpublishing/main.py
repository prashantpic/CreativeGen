"""
Main application file for the FastAPI service. Initializes the FastAPI app,
includes routers, and sets up middleware and event handlers.
"""

import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from .api.v1.routers import connections_router, insights_router, publishing_router
from .application.exceptions import SocialPublishingBaseError
from .config import get_settings
from .infrastructure.database.session_manager import DBSessionManager
from .infrastructure.logging.config import setup_logging

# --- App Initialization ---

# Load settings first, as they are used by other initializers
settings = get_settings()

# Setup structured logging
setup_logging(settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Create FastAPI app instance
app = FastAPI(
    title="CreativeFlow Social Publishing Service",
    description="This service manages social media connections, publishing, and insights.",
    version="1.0.0",
)


# --- Event Handlers ---

@app.on_event("startup")
async def startup_event():
    """
    Application startup logic.
    Initializes the database connection pool.
    """
    logger.info("Starting up Social Publishing Service...")
    DBSessionManager.init_db(settings.DATABASE_URL)
    logger.info("Database session manager initialized.")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown logic.
    Closes the database connection pool.
    """
    logger.info("Shutting down Social Publishing Service...")
    await DBSessionManager.close_engine()
    logger.info("Database engine closed.")


# --- Exception Handlers ---

@app.exception_handler(SocialPublishingBaseError)
async def handle_custom_application_errors(
    request: Request, exc: SocialPublishingBaseError
):
    """
    Global exception handler for custom application errors.
    Returns a structured JSON error response.
    """
    # This can be expanded to map specific exceptions to status codes
    status_code = status.HTTP_400_BAD_REQUEST
    from .application.exceptions import (
        ConnectionNotFoundError,
        JobNotFoundError,
        PermissionDeniedError,
        TokenExpiredError,
        InsufficientPermissionsError
    )
    if isinstance(exc, (ConnectionNotFoundError, JobNotFoundError)):
        status_code = status.HTTP_404_NOT_FOUND
    if isinstance(exc, (PermissionDeniedError, InsufficientPermissionsError, TokenExpiredError)):
        status_code = status.HTTP_403_FORBIDDEN


    logger.warning("Application error occurred: %s", exc, exc_info=True)
    return JSONResponse(
        status_code=status_code,
        content={"code": exc.__class__.__name__, "detail": str(exc)},
    )


@app.exception_handler(Exception)
async def handle_generic_errors(request: Request, exc: Exception):
    """
    Generic exception handler for unhandled errors.
    Returns a 500 Internal Server Error response.
    """
    logger.error("An unhandled exception occurred: %s", exc, exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"code": "internal_server_error", "detail": "An unexpected error occurred."},
    )


# --- API Routers ---

app.include_router(
    connections_router.router,
    prefix="/api/v1/connections",
    tags=["Social Connections"],
)
app.include_router(
    publishing_router.router,
    prefix="/api/v1/publishing",
    tags=["Content Publishing"],
)
app.include_router(
    insights_router.router,
    prefix="/api/v1/insights",
    tags=["Content Insights"],
)

@app.get("/health", tags=["Health Check"])
async def health_check():
    """
    Simple health check endpoint.
    """
    return {"status": "ok"}