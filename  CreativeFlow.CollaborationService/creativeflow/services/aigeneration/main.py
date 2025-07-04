import logging
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from creativeflow.services.aigeneration.api.v1.endpoints import generation_requests, n8n_callbacks
from creativeflow.services.aigeneration.core import dependencies
from creativeflow.services.aigeneration.core.config import settings
from creativeflow.services.aigeneration.core.error_handlers import setup_error_handlers
from creativeflow.services.aigeneration.core.logging_config import setup_logging
from creativeflow.services.aigeneration.infrastructure.database.db_config import init_db
from creativeflow.services.aigeneration.infrastructure.messaging.rabbitmq_publisher import RabbitMQPublisher

# --- Setup Logging ---
# This must be called before the app is created to ensure logs are formatted correctly from the start.
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.
    - Initializes database tables.
    - Connects to RabbitMQ.
    - Creates a shared HTTP client.
    - Cleans up connections on shutdown.
    """
    logger.info("Application starting up...")
    
    # Initialize Database
    await init_db()
    
    # Initialize RabbitMQ Publisher
    rabbitmq_publisher = RabbitMQPublisher(amqp_url=settings.RABBITMQ_URL)
    try:
        rabbitmq_publisher.connect()
        dependencies.rabbitmq_publisher_instance = rabbitmq_publisher
    except Exception as e:
        logger.critical("Failed to connect to RabbitMQ on startup: %s", e)
        # Decide if the app should fail to start if MQ is down
        # For now, we allow it to start but publishing will fail.
        dependencies.rabbitmq_publisher_instance = None
        
    # Initialize shared HTTP Client
    dependencies.http_client_instance = httpx.AsyncClient()
    
    yield  # --- Application is now running ---
    
    logger.info("Application shutting down...")
    
    # Close RabbitMQ connection
    if dependencies.rabbitmq_publisher_instance:
        dependencies.rabbitmq_publisher_instance.close()
        
    # Close shared HTTP Client
    if dependencies.http_client_instance:
        await dependencies.http_client_instance.aclose()


# --- Create FastAPI App ---
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)


# --- Configure Middleware ---
# Set all origins to allow all for simple deployment.
# In production, this should be a list of allowed origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Register Error Handlers ---
setup_error_handlers(app)


# --- Include API Routers ---
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


@app.get("/", tags=["Health Check"])
async def read_root():
    """A simple health check endpoint."""
    return {"status": "ok", "service": settings.PROJECT_NAME}


# --- Uvicorn entrypoint for local development ---
if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Uvicorn server for local development...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)