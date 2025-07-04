import logging
import uvicorn
import httpx

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from creativeflow.services.aigeneration.core.config import settings
from creativeflow.services.aigeneration.core.logging_config import setup_logging
from creativeflow.services.aigeneration.core.dependencies import app_state, get_rabbitmq_publisher
from creativeflow.services.aigeneration.core import error_handlers
from creativeflow.services.aigeneration.api.v1.endpoints import generation_requests, n8n_callbacks
from creativeflow.services.aigeneration.infrastructure.database.db_config import init_db
from creativeflow.services.aigeneration.infrastructure.messaging.rabbitmq_publisher import RabbitMQPublisher


# Setup logging before anything else
setup_logging()
logger = logging.getLogger(__name__)

# Create FastAPI app instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    version="1.0.0"
)

# --- Event Handlers ---

@app.on_event("startup")
async def startup_event():
    """
    Application startup logic.
    - Initializes the database (creates tables if they don't exist).
    - Connects the RabbitMQ publisher.
    - Creates a shared httpx client.
    """
    logger.info("Application startup...")
    try:
        await init_db()
        logger.info("Database initialized.")
    except Exception as e:
        logger.exception("Failed to initialize database.", exc_info=e)

    try:
        publisher = RabbitMQPublisher(
            amqp_url=settings.RABBITMQ_URL,
            exchange_name=settings.RABBITMQ_GENERATION_EXCHANGE,
            queue_name=settings.RABBITMQ_N8N_JOB_QUEUE,
            routing_key=settings.RABBITMQ_N8N_JOB_ROUTING_KEY
        )
        publisher.connect()
        app_state["rabbitmq_publisher"] = publisher
        logger.info("RabbitMQ publisher connected.")
    except Exception as e:
        logger.exception("Failed to connect RabbitMQ publisher.", exc_info=e)
        
    app_state["httpx_client"] = httpx.AsyncClient()
    logger.info("Shared HTTPX client created.")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown logic.
    - Closes the RabbitMQ publisher connection.
    - Closes the shared httpx client.
    """
    logger.info("Application shutdown...")
    publisher = app_state.get("rabbitmq_publisher")
    if publisher:
        publisher.close()
        logger.info("RabbitMQ publisher connection closed.")
        
    http_client = app_state.get("httpx_client")
    if http_client:
        await http_client.aclose()
        logger.info("Shared HTTPX client closed.")

# --- Middleware ---

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# --- Exception Handlers ---

app.add_exception_handler(RequestValidationError, error_handlers.validation_exception_handler)
app.add_exception_handler(error_handlers.ResourceNotFoundError, error_handlers.resource_not_found_exception_handler)
app.add_exception_handler(error_handlers.InsufficientCreditsError, error_handlers.insufficient_credits_exception_handler)
app.add_exception_handler(error_handlers.InvalidStateError, error_handlers.invalid_state_exception_handler)
app.add_exception_handler(Exception, error_handlers.http_exception_handler)


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

@app.get("/", summary="Health Check")
def read_root():
    """
    Root endpoint for health checks.
    """
    return {"status": "ok", "project_name": settings.PROJECT_NAME}

# --- Main entry point for Uvicorn ---
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level=settings.LOG_LEVEL.lower()
    )