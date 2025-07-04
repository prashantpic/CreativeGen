import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from api.main import api_router as main_api_router
from core.config import get_settings
from core.exceptions import AppException
from core.logging_config import setup_logging
from infrastructure.cache.redis_client import redis_client
from infrastructure.external_clients.ai_generation_client import ai_generation_client
from infrastructure.external_clients.asset_management_client import (
    asset_management_client,
)
from infrastructure.external_clients.user_team_client import user_team_client
from infrastructure.messaging.rabbitmq_client import rabbitmq_client

# Get a logger instance for this module
logger = logging.getLogger(__name__)


# --- Exception Handlers ---

async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """
    Global handler for custom application exceptions (AppException).
    Returns a JSON response with the status code and detail from the exception.
    """
    logger.warning(
        f"Application error occurred: {exc.detail}",
        extra={"status_code": exc.status_code, "detail": exc.detail},
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def sqlalchemy_exception_handler(
    request: Request, exc: SQLAlchemyError
) -> JSONResponse:
    """
    Global handler for SQLAlchemy database exceptions.
    Logs the detailed error and returns a generic 500 error to the client.
    """
    # Note: In production, do not expose raw exception details.
    logger.error(
        f"Database error occurred: {exc}",
        exc_info=True,
        extra={"error_type": type(exc).__name__},
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal database error occurred."},
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Global handler for Pydantic's RequestValidationError.
    Returns a 422 Unprocessable Entity response with detailed validation errors.
    """
    logger.warning(
        f"Request validation error: {exc.errors()}", extra={"errors": exc.errors()}
    )
    # Re-structure the error for a more user-friendly format if needed
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Validation Error", "errors": exc.errors()},
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global handler for any other unhandled exceptions.
    Logs the full exception and returns a generic 500 error.
    """
    logger.error(
        f"An unhandled exception occurred: {exc}",
        exc_info=True,
        extra={"error_type": type(exc).__name__},
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected internal server error occurred."},
    )


# --- Lifespan Management ---

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages application startup and shutdown events.
    This is the modern way to handle lifespan events in FastAPI,
    ensuring resources are initialized before serving requests and
    cleaned up gracefully on shutdown.
    """
    settings = get_settings()
    logger.info("Service starting up...")

    # Initialize connections
    try:
        await rabbitmq_client.connect(settings.RABBITMQ_URL)
        logger.info("RabbitMQ client connected successfully.")

        await redis_client.connect()
        logger.info("Redis client connected successfully.")

        ai_generation_client.initialize(settings.AI_GENERATION_SERVICE_URL)
        logger.info("AI Generation HTTP client initialized.")

        asset_management_client.initialize(settings.ASSET_MANAGEMENT_SERVICE_URL)
        logger.info("Asset Management HTTP client initialized.")

        user_team_client.initialize(settings.USER_TEAM_SERVICE_URL)
        logger.info("User/Team Management HTTP client initialized.")

    except Exception as e:
        logger.critical(f"Failed to initialize resources during startup: {e}", exc_info=True)
        # Raise the exception to prevent the service from starting in a broken state.
        raise

    yield  # The application is now running and can serve requests

    # Shutdown logic
    logger.info("Service shutting down...")
    try:
        await rabbitmq_client.close()
        logger.info("RabbitMQ client disconnected.")
        await redis_client.close()
        logger.info("Redis client disconnected.")
        await ai_generation_client.close()
        logger.info("AI Generation HTTP client closed.")
        await asset_management_client.close()
        logger.info("Asset Management HTTP client closed.")
        await user_team_client.close()
        logger.info("User/Team Management HTTP client closed.")
    except Exception as e:
        logger.error(f"Error during resource cleanup on shutdown: {e}", exc_info=True)


# --- Application Factory ---

def create_application() -> FastAPI:
    """
    Creates and configures the FastAPI application instance.
    This factory pattern allows for easier testing and configuration management.
    """
    settings = get_settings()

    # Configure structured logging as early as possible
    setup_logging(log_level=settings.LOG_LEVEL)

    # Create FastAPI app instance with lifespan management
    app = FastAPI(
        title="CreativeFlow Developer Platform Service",
        description="Manages API keys, webhooks, usage, and proxies API requests for third-party developers.",
        version="1.0.0",
        lifespan=lifespan,
    )

    # Add CORS middleware to allow cross-origin requests
    # In production, this should be restricted to known origins.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # WARNING: Restrict this in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include the main API router which aggregates all other routers
    app.include_router(main_api_router)

    # Add custom global exception handlers
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    logger.info("FastAPI application created and configured successfully.")
    return app


# Create the app instance using the factory
app = create_application()

# --- Health Check Endpoint ---
@app.get("/health", tags=["Monitoring"], status_code=status.HTTP_200_OK)
async def health_check():
    """Simple health check endpoint to verify the service is running."""
    return {"status": "ok"}


# --- Uvicorn Runner (for local development) ---
if __name__ == "__main__":
    # This block is for running the application directly for development.
    # For production, use a process manager like Gunicorn with Uvicorn workers.
    # Example: gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
    settings = get_settings()
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level=settings.LOG_LEVEL.lower(),
    )