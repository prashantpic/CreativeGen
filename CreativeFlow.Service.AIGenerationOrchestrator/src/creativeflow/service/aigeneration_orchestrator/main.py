"""
The main entry point for the FastAPI application. This file initializes the
FastAPI app, sets up middleware, includes API routers, defines application
lifecycle events, and wires up dependencies.
"""
import logging
import time
import uuid
from contextlib import asynccontextmanager

import httpx
from aio_pika.abc import AbstractRobustConnection
from fastapi import FastAPI, Request, Response
from python_json_logger import jsonlogger

from .api.v1.endpoints import callbacks, generation
from .api.v1.dependencies import AppDependencies
from .infrastructure.messaging.pika_publisher import get_pika_connection


# --- Logging Configuration ---
# Configure structured JSON logging
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    "%(asctime)s %(name)s %(levelname)s %(message)s %(correlation_id)s"
)
logHandler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO, handlers=[logHandler])
logger = logging.getLogger(__name__)


# --- Application Lifecycle (Startup/Shutdown) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages application startup and shutdown events.
    - Creates a persistent HTTP client.
    - Establishes a connection to RabbitMQ.
    - Cleans up resources on shutdown.
    """
    # Startup
    logger.info("Application startup...")
    http_client = httpx.AsyncClient()
    pika_connection = await get_pika_connection()
    AppDependencies.set_http_client(http_client)
    AppDependencies.set_pika_connection(pika_connection)
    logger.info("HTTP client and Pika connection initialized.")
    yield
    # Shutdown
    logger.info("Application shutdown...")
    await http_client.aclose()
    await pika_connection.close()
    logger.info("HTTP client and Pika connection closed.")


# --- FastAPI App Initialization ---
app = FastAPI(
    title="CreativeFlow AI Generation Orchestrator",
    description="Service to orchestrate AI creative generation workflows.",
    version="1.0.0",
    lifespan=lifespan,
)


# --- Middleware Configuration ---
@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    """
    Injects a correlation ID into every request and log message for distributed tracing.
    """
    correlation_id = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
    
    # Add correlation_id to the request state to be accessible in dependencies/endpoints
    request.state.correlation_id = correlation_id
    
    # For structured logging
    logger.info("Request started", extra={"correlation_id": correlation_id})
    
    response = await call_next(request)
    response.headers["X-Correlation-ID"] = correlation_id
    return response


@app.middleware("http")
async def logging_and_error_middleware(request: Request, call_next):
    """
    Centralized middleware for logging requests/responses and handling all
    uncaught exceptions.
    """
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        logger.info(
            f"Request {request.method} {request.url.path} completed in {process_time:.2f}ms. Status: {response.status_code}",
            extra={"correlation_id": getattr(request.state, "correlation_id", "N/A")}
        )
        return response
    except Exception as e:
        logger.critical(
            f"Unhandled exception for request {request.method} {request.url.path}: {e}",
            exc_info=True,
            extra={"correlation_id": getattr(request.state, "correlation_id", "N/A")}
        )
        return Response(
            content='{"error": "Internal Server Error"}',
            status_code=500,
            media_type="application/json",
        )


# --- API Routers ---
app.include_router(
    generation.router,
    prefix="/api/v1/generations",
    tags=["Generations"],
)
app.include_router(
    callbacks.router,
    prefix="/api/v1/callbacks",
    tags=["Callbacks"],
)


@app.get("/health", tags=["Health Check"])
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}