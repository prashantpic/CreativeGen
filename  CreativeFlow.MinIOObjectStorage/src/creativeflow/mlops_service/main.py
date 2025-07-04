"""
Main application file for the FastAPI MLOps service.

This file initializes the FastAPI application, mounts the API routers for different
versions, sets up logging, and configures global middleware and exception handlers.
It also manages application lifecycle events like startup and shutdown.
"""
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from creativeflow.mlops_service.api.v1.endpoints import (
    deployments,
    feedback,
    models,
    validation,
)
from creativeflow.mlops_service.core.config import get_settings
from creativeflow.mlops_service.database import engine
from creativeflow.mlops_service.infrastructure.database.orm_models import ai_model_orm
from creativeflow.mlops_service.utils.exceptions import MLOpsServiceException
from creativeflow.mlops_service.utils.logging_config import setup_logging

# Create the database tables if they don't exist.
# In a production setup, this would be handled by Alembic migrations.
# ai_model_orm.Base.metadata.create_all(bind=engine)

# Get application settings
settings = get_settings()

# Setup structured logging
setup_logging(log_level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


def create_application() -> FastAPI:
    """
    Creates and configures the FastAPI application instance.
    """
    app = FastAPI(
        title="CreativeFlow MLOps Service",
        description="Manages the lifecycle of custom AI models for the CreativeFlow platform.",
        version="1.0.0",
        docs_url="/api/v1/mlops/docs",
        redoc_url="/api/v1/mlops/redoc",
        openapi_url="/api/v1/mlops/openapi.json",
    )

    # Add routers for v1
    api_v1_prefix = "/api/v1/mlops"
    app.include_router(models.router, prefix=f"{api_v1_prefix}/models", tags=["Models"])
    app.include_router(deployments.router, prefix=f"{api_v1_prefix}/deployments", tags=["Deployments"])
    app.include_router(validation.router, prefix=f"{api_v1_prefix}/validation", tags=["Validation"])
    app.include_router(feedback.router, prefix=f"{api_v1_prefix}/feedback", tags=["Feedback"])

    return app


app = create_application()


@app.on_event("startup")
async def on_startup():
    """
    Application startup event handler.
    Initializes connections to external services.
    """
    logger.info("MLOps Service is starting up...")
    # Here you would initialize clients for MinIO, Kubernetes, etc.
    # These are handled via dependency injection in this project structure,
    # so we'll just log the startup.
    logger.info("MLOps Service startup complete.")


@app.on_event("shutdown")
async def on_shutdown():
    """
    Application shutdown event handler.
    Closes connections gracefully.
    """
    logger.info("MLOps Service is shutting down...")
    # Gracefully close any connections if needed
    logger.info("MLOps Service shutdown complete.")


@app.exception_handler(MLOpsServiceException)
async def mlops_service_exception_handler(request: Request, exc: MLOpsServiceException):
    """
    Global exception handler for custom MLOpsServiceException.
    Returns a structured JSON error response.
    """
    logger.error(f"MLOps service error: {exc.detail}", exc_info=exc)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.get("/health", tags=["Health Check"])
async def health_check():
    """
    Simple health check endpoint to verify the service is running.
    """
    return {"status": "ok"}