import logging
import uvicorn
import httpx
from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .core.logging_config import setup_logging
from .core.error_handlers import (
    validation_exception_handler,
    custom_app_exception_handler,
    http_exception_handler,
    generic_exception_handler,
    ApplicationException,
)
from .infrastructure.database.db_config import init_db
from .infrastructure.messaging.rabbitmq_publisher import RabbitMQPublisher
from .api.v1.endpoints import generation_requests, n8n_callbacks

# Setup logging as early as possible
setup_logging(settings)

# Create FastAPI app instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# --- Middleware ---
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# --- Event Handlers (Startup/Shutdown) ---
@app.on_event("startup")
async def startup_event():
    """
    Application startup logic:
    - Initialize database tables.
    - Connect to RabbitMQ.
    - Create singleton HTTP client.
    """
    logging.info("Starting up application...")
    
    # Initialize database
    # In a production setup, you would use Alembic for migrations.
    # This is suitable for development/testing.
    await init_db()
    logging.info("Database initialized.")

    # Create and connect RabbitMQ publisher
    rabbitmq_publisher = RabbitMQPublisher(settings.RABBITMQ_URL)
    await rabbitmq_publisher.connect()
    app.state.rabbitmq_publisher = rabbitmq_publisher
    logging.info("RabbitMQ publisher connected and available in app.state.")
    
    # Create singleton httpx client
    app.state.http_client = httpx.AsyncClient()
    logging.info("httpx.AsyncClient created and available in app.state.")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown logic:
    - Close RabbitMQ connection.
    - Close HTTP client.
    """
    logging.info("Shutting down application...")
    
    # Close RabbitMQ connection
    if hasattr(app.state, 'rabbitmq_publisher') and app.state.rabbitmq_publisher:
        await app.state.rabbitmq_publisher.close()
    
    # Close httpx client
    if hasattr(app.state, 'http_client') and app.state.http_client:
        await app.state.http_client.aclose()
        
    logging.info("Shutdown complete.")


# --- Exception Handlers ---
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(ApplicationException, custom_app_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


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

@app.get("/", summary="Health Check", tags=["Health"])
def read_root():
    """
    Root endpoint for health checks.
    """
    return {"status": "ok", "service": settings.PROJECT_NAME}


# --- Main entry point for Uvicorn ---
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True, # Use reload for development
        log_level=settings.LOG_LEVEL.lower()
    )