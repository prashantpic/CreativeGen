"""
Main Application Entrypoint for the FastAPI Service.

This file initializes the FastAPI application, sets up logging, includes API
routers, configures middleware (like CORS), registers custom error handlers,
and defines application startup and shutdown event handlers.
"""
import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1.endpoints import generation_requests, n8n_callbacks
from .core.config import settings
from .core.dependencies import http_client_instance, rabbitmq_publisher_instance
from .core.error_handlers import add_exception_handlers
from .core.logging_config import setup_logging
from .infrastructure.database.db_config import init_db

# --- Application Setup ---
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    version="1.0.0"
)

# --- Middleware ---
# Configure CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Event Handlers ---
@app.on_event("startup")
async def startup_event():
    """
    Application startup logic.
    - Initialize database tables (for development).
    - Connect to RabbitMQ.
    """
    logger.info("Application startup...")
    # init_db() # Uncomment for easy dev setup. In prod, use Alembic migrations.
    try:
        await rabbitmq_publisher_instance.connect()
    except Exception as e:
        logger.critical(f"Failed to connect to RabbitMQ on startup: {e}", exc_info=True)
        # Depending on requirements, you might want the app to fail startup if MQ is down.
        # For now, it will log a critical error and continue.
    logger.info("Application startup complete.")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown logic.
    - Gracefully close connections.
    """
    logger.info("Application shutdown...")
    await http_client_instance.aclose()
    await rabbitmq_publisher_instance.close()
    logger.info("Application shutdown complete.")

# --- Error Handling ---
add_exception_handlers(app)

# --- API Routers ---
app.include_router(
    generation_requests.router,
    prefix=f"{settings.API_V1_STR}/generation-requests",
    tags=["Generation Requests"]
)
app.include_router(
    n8n_callbacks.router,
    prefix=f"{settings.API_V1_STR}/n8n-callbacks",
    tags=["n8n Callbacks"]
)

# --- Root Endpoint ---
@app.get("/", tags=["Health Check"])
async def read_root():
    """A simple health check endpoint."""
    return {"status": "ok", "service": settings.PROJECT_NAME}

# --- Main execution block (for direct execution) ---
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable reload for development
        log_config=None # Disable uvicorn's default logging to use our custom setup
    )