import logging
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from creativeflow.services.aigeneration.core.config import settings
from creativeflow.services.aigeneration.core.logging_config import setup_logging
from creativeflow.services.aigeneration.core.error_handlers import add_exception_handlers
from creativeflow.services.aigeneration.api.v1.endpoints import generation_requests, n8n_callbacks
from creativeflow.services.aigeneration.infrastructure.database.db_config import init_db
from creativeflow.services.aigeneration.infrastructure.messaging.rabbitmq_publisher import RabbitMQPublisher
from creativeflow.services.aigeneration.application.services.credit_service_client import get_credit_service_client
from creativeflow.services.aigeneration.application.services.notification_service_client import get_notification_service_client

# Setup logging first
setup_logging()
logger = logging.getLogger(__name__)

# Create FastAPI app instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# --- Middleware ---
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
    Application startup logic:
    - Initialize database connection and tables.
    - Initialize RabbitMQ publisher connection.
    - Initialize HTTP clients.
    """
    logger.info("Application startup...")
    await init_db()
    
    # Initialize RabbitMQ Publisher and store in app state
    rabbitmq_publisher = RabbitMQPublisher(
        amqp_url=settings.RABBITMQ_URL,
        exchange_name=settings.RABBITMQ_GENERATION_EXCHANGE
    )
    await rabbitmq_publisher.connect()
    app.state.rabbitmq_publisher = rabbitmq_publisher
    
    # Initialize HTTP clients to establish connection pools
    app.state.credit_service_client = get_credit_service_client()
    app.state.notification_service_client = get_notification_service_client()

    logger.info("Application startup complete.")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown logic:
    - Gracefully close RabbitMQ connection.
    - Gracefully close HTTP client connections.
    """
    logger.info("Application shutdown...")
    if hasattr(app.state, 'rabbitmq_publisher') and app.state.rabbitmq_publisher:
        await app.state.rabbitmq_publisher.close()
    
    if hasattr(app.state, 'credit_service_client') and app.state.credit_service_client:
        await app.state.credit_service_client.close()

    if hasattr(app.state, 'notification_service_client') and app.state.notification_service_client:
        await app.state.notification_service_client.close()
        
    logger.info("Application shutdown complete.")

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
async def read_root():
    return {"status": "ok", "service": settings.PROJECT_NAME}

# --- Main execution ---
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True, # Use reload for development
        log_config=None # Disable uvicorn's default logging to use our custom setup
    )