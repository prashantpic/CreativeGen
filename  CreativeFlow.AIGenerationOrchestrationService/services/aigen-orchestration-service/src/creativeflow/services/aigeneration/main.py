"""
Main application entrypoint for the FastAPI AI Generation Orchestration Service.

This file initializes the FastAPI application, includes the API routers,
configures middleware, and sets up startup/shutdown event handlers for
managing resources like database connections and message queue publishers.
"""

import logging
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

# Import project components
from creativeflow.services.aigeneration.api.v1.endpoints import generation_requests, n8n_callbacks
from creativeflow.services.aigeneration.core.config import settings
from creativeflow.services.aigeneration.core.error_handlers import (
    ApplicationException,
    application_exception_handler,
    http_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)
from creativeflow.services.aigeneration.core.logging_config import setup_logging
from creativeflow.services.aigeneration.infrastructure.database.db_config import close_db_engine, init_db
from creativeflow.services.aigeneration.infrastructure.messaging.rabbitmq_publisher import rabbitmq_publisher

# Configure logging as per SDS Section 10
setup_logging(log_level=settings.LOG_LEVEL, log_format=settings.LOG_FORMAT)
logger = logging.getLogger(__name__)


# Initialize FastAPI application as per SDS Section 14
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# --- Middleware ---
# Configure CORS Middleware for cross-origin requests from the frontend.
# In a production environment, this should be restricted to the specific frontend domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods.
    allow_headers=["*"],  # Allows all headers.
)


# --- Event Handlers (Startup/Shutdown) ---
@app.on_event("startup")
async def startup_event():
    """
    Handles application startup logic.
    - Initializes the database engine.
    - Connects to the RabbitMQ server.
    """
    logger.info(f"Starting up {settings.PROJECT_NAME}...")
    try:
        await init_db()
        logger.info("Database engine initialized successfully.")
    except Exception as e:
        logger.critical(f"FATAL: Could not initialize database engine: {e}", exc_info=True)
        # Depending on the deployment strategy, you might want the app to fail
        # fast if a critical dependency like the database is unavailable.
        # import os, signal
        # os.kill(os.getpid(), signal.SIGTERM)

    try:
        await rabbitmq_publisher.connect()
        logger.info("RabbitMQ publisher connected successfully.")
    except Exception as e:
        logger.critical(f"FATAL: Could not connect to RabbitMQ: {e}", exc_info=True)
        # import os, signal
        # os.kill(os.getpid(), signal.SIGTERM)


@app.on_event("shutdown")
async def shutdown_event():
    """
    Handles application shutdown logic.
    - Gracefully closes the RabbitMQ connection.
    - Gracefully closes the database engine connections.
    """
    logger.info(f"Shutting down {settings.PROJECT_NAME}...")
    try:
        await rabbitmq_publisher.close()
        logger.info("RabbitMQ publisher connection closed.")
    except Exception as e:
        logger.error(f"Error closing RabbitMQ connection: {e}", exc_info=True)

    try:
        await close_db_engine()
        logger.info("Database engine connections closed.")
    except Exception as e:
        logger.error(f"Error closing database engine connections: {e}", exc_info=True)


# --- Exception Handlers ---
# Register custom exception handlers as per SDS Section 9 for consistent error responses.
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(ApplicationException, application_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)  # Catch-all for unexpected errors


# --- API Routers ---
# Include API routers as per SDS Section 14
app.include_router(
    generation_requests.router,
    prefix=f"{settings.API_V1_STR}/generation-requests",
    tags=["Generation Requests"],
)
app.include_router(
    n8n_callbacks.router,
    prefix=f"{settings.API_V1_STR}/n8n-callbacks",
    tags=["n8n Callbacks"],
)


# --- Root/Health Check Endpoint ---
@app.get("/", tags=["Health Check"])
async def root():
    """
    A simple health check endpoint to verify that the service is running.
    """
    return {"status": "ok", "service": settings.PROJECT_NAME}


# --- Uvicorn Runner ---
# This block allows running the app directly using `python main.py` for development.
if __name__ == "__main__":
    is_debug_mode = settings.LOG_LEVEL.upper() == "DEBUG"
    uvicorn.run(
        "creativeflow.services.aigeneration.main:app",
        host="0.0.0.0",
        port=8000,
        reload=is_debug_mode,  # Enable auto-reload only in DEBUG mode
        log_level=settings.LOG_LEVEL.lower(),
    )