"""
Main application file for the FastAPI MLOps service.

This file initializes the FastAPI application, mounts the API routers,
sets up middleware, and defines global configurations and event handlers.
"""
import logging
import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from creativeflow.mlops_service.api.v1.endpoints import (
    deployments, feedback, models, validation
)
from creativeflow.mlops_service.utils.exceptions import MLOpsServiceException
from creativeflow.mlops_service.utils.logging_config import setup_logging
from creativeflow.mlops_service.core.config import get_settings

# Setup logging
settings = get_settings()
setup_logging(log_level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Create FastAPI app instance
app = FastAPI(
    title="CreativeFlow MLOps Service",
    description="Manages the lifecycle of custom AI models within the CreativeFlow platform.",
    version="1.0.0"
)

# --- Middleware ---
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware to log request details and processing time."""
    start_time = time.time()
    logger.info(f"Request started: {request.method} {request.url.path}")
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    logger.info(
        f"Request finished: {request.method} {request.url.path} "
        f"Status: {response.status_code} "
        f"Took: {process_time:.2f}ms"
    )
    return response

# --- Exception Handlers ---
@app.exception_handler(MLOpsServiceException)
async def mlops_service_exception_handler(request: Request, exc: MLOpsServiceException):
    """Custom exception handler for all service-specific exceptions."""
    logger.error(f"Error processing request {request.url.path}: {exc.detail}", exc_info=False)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# --- API Routers ---
api_prefix = "/api/v1/mlops"
app.include_router(models.router, prefix=f"{api_prefix}/models", tags=["Models & Versions"])
app.include_router(deployments.router, prefix=f"{api_prefix}/deployments", tags=["Deployments"])
app.include_router(validation.router, prefix=f"{api_prefix}/validation", tags=["Validation"])
app.include_router(feedback.router, prefix=f"{api_prefix}/feedback", tags=["Feedback"])

# --- Lifecycle Events ---
@app.on_event("startup")
async def on_startup():
    """Actions to perform on application startup."""
    logger.info("MLOps Service is starting up...")
    # Initialization of clients (MinIO, K8s, etc.) is handled within their adapters
    # to allow for easier dependency injection and testing.
    logger.info("MLOps Service startup complete.")

@app.on_event("shutdown")
async def on_shutdown():
    """Actions to perform on application shutdown."""
    logger.info("MLOps Service is shutting down...")
    # Add any necessary cleanup here.
    logger.info("MLOps Service shutdown complete.")

# --- Root Endpoint ---
@app.get("/", summary="Health Check", tags=["Health"])
async def root():
    """A simple health check endpoint."""
    return {"status": "ok", "service": "CreativeFlow.MLOpsService"}