import logging
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from creativeflow.services.aigeneration.api.v1.endpoints import generation_requests, n8n_callbacks
from creativeflow.services.aigeneration.core.config import settings
from creativeflow.services.aigeneration.core.error_handlers import add_exception_handlers
from creativeflow.services.aigeneration.core.logging_config import setup_logging
from creativeflow.services.aigeneration.infrastructure.database.db_config import init_db
from creativeflow.services.aigeneration.infrastructure.messaging.rabbitmq_publisher import RabbitMQPublisher

# Setup logging configuration
setup_logging()
logger = logging.getLogger(__name__)

# Create FastAPI app instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# --- Event Handlers ---
@app.on_event("startup")
async def startup_event():
    """
    Application startup event handler.
    Initializes database and RabbitMQ publisher connection.
    """
    logger.info("Starting up service...")
    try:
        await init_db()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.critical(f"Database initialization failed: {e}", exc_info=True)

    try:
        RabbitMQPublisher.get_instance() # This will initialize the connection
        logger.info("RabbitMQ publisher initialized successfully.")
    except Exception as e:
        logger.critical(f"RabbitMQ publisher initialization failed: {e}", exc_info=True)
    logger.info("Service startup complete.")


@app.on_event("shutdown")
def shutdown_event():
    """
    Application shutdown event handler.
    Gracefully closes RabbitMQ connection.
    """
    logger.info("Shutting down service...")
    try:
        rabbitmq_publisher = RabbitMQPublisher.get_instance()
        if rabbitmq_publisher:
            rabbitmq_publisher.close()
        logger.info("RabbitMQ connection closed.")
    except Exception as e:
        logger.error(f"Error during RabbitMQ shutdown: {e}", exc_info=True)
    logger.info("Service shutdown complete.")


# --- Middleware ---
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Error Handlers ---
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


@app.get("/", tags=["Health Check"])
def read_root():
    """
    Root endpoint for health checks.
    """
    return {"status": "ok", "service": settings.PROJECT_NAME}


if __name__ == "__main__":
    # Run the application using Uvicorn
    uvicorn.run(
        "creativeflow.services.aigeneration.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Set to False in production
    )