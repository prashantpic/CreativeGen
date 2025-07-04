```python
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from api.main import api_router
from core.config import get_settings, Settings
from core.exceptions import AppException
from core.logging_config import setup_logging
from infrastructure.cache.redis_client import redis_client
from infrastructure.external_clients.ai_generation_client import ai_generation_client
from infrastructure.external_clients.asset_management_client import asset_management_client
from infrastructure.external_clients.user_team_client import user_team_client
from infrastructure.messaging.rabbitmq_client import rabbitmq_client

# Initialize logger
logger = logging.getLogger(__name__)

# --- Event Handlers ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.
    """
    settings = get_settings()
    logger.info("Starting up Developer Platform Service...")

    # Initialize external clients
    try:
        await redis_client.connect(settings.REDIS_URL)
        logger.info("Redis client connected.")
        await rabbitmq_client.connect(settings.RABBITMQ_URL)
        logger.info("RabbitMQ client connected.")
        ai_generation_client.init_client(settings.AI_GENERATION_SERVICE_URL)
        asset_management_client.init_client(settings.ASSET_MANAGEMENT_SERVICE_URL)
        user_team_client.init_client(settings.USER_TEAM_SERVICE_URL)
        logger.info("HTTP clients initialized.")
    except Exception as e:
        logger.critical(f"Failed to initialize critical infrastructure: {e}", exc_info=True)
        # Depending on the policy, we might want to exit the application
        # raise SystemExit(f"Critical infrastructure failure: {e}") from e

    yield

    logger.info("Shutting down Developer Platform Service...")
    # Clean up resources
    await redis_client.close()
    logger.info("Redis client disconnected.")
    await rabbitmq_client.close()
    logger.info("RabbitMQ client disconnected.")
    await ai_generation_client.close_client()
    await asset_management_client.close_client()
    await user_team_client.close_client()
    logger.info("HTTP clients closed.")


# --- Exception Handlers ---
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handles custom application exceptions."""
    logger.warning(f"Application error occurred: {exc.detail} for request {request.method} {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """Handles database exceptions."""
    logger.error(f"Database error occurred: {exc} for request {request.method} {request.url.path}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal database error occurred."},
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handles Pydantic validation errors."""
    logger.warning(f"Request validation error: {exc.errors()} for request {request.method} {request.url.path}")
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation Error", "errors": exc.errors()},
    )

async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handles any other unexpected exceptions."""
    logger.critical(f"Unhandled exception: {exc} for request {request.method} {request.url.path}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected internal server error occurred."},
    )

def create_application() -> FastAPI:
    """
    Creates and configures the FastAPI application instance.
    """
    settings = get_settings()
    setup_logging(log_level=settings.LOG_LEVEL)

    app = FastAPI(
        title="CreativeFlow Developer Platform Service",
        description="Manages third-party developer access, API keys, webhooks, and proxies API requests.",
        version="1.0.0",
        lifespan=lifespan,
    )

    # Add Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Adjust for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include Routers
    app.include_router(api_router, prefix="/api/v1")

    # Register Exception Handlers
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    logger.info("FastAPI application created and configured.")
    return app


app = create_application()

@app.get("/health", tags=["Health Check"])
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}