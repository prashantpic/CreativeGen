import logging
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .core.logging_config import setup_logging
from .core.error_handlers import setup_error_handlers
from .core.dependencies import get_rabbitmq_publisher
from .api.v1.endpoints import generation_requests, n8n_callbacks
from .infrastructure.database.db_config import init_db

# --- Initialize Logging ---
# This should be one of the first things to run
setup_logging()
logger = logging.getLogger(__name__)

# --- FastAPI Application Instance ---
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    version="1.0.0"
)

# --- Middleware ---
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# --- Error Handlers ---
setup_error_handlers(app)

# --- API Routers ---
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

# --- Startup and Shutdown Events ---
@app.on_event("startup")
async def startup_event():
    """
    Actions to perform on application startup.
    - Initialize database tables (in dev/test).
    - Establish initial connection to RabbitMQ.
    """
    logger.info("Application startup...")
    # In a real app with migrations, you might not call init_db() here.
    # await init_db() 
    
    # Eagerly connect to RabbitMQ to fail fast if it's unavailable.
    try:
        get_rabbitmq_publisher()._ensure_connection()
        logger.info("RabbitMQ publisher connection confirmed.")
    except Exception as e:
        logger.critical(f"Could not connect to RabbitMQ on startup: {e}", exc_info=True)
        # Depending on the policy, you might want to exit the application here.
    logger.info("Application startup complete.")

@app.on_event("shutdown")
def shutdown_event():
    """
    Actions to perform on application shutdown.
    - Gracefully close connections.
    """
    logger.info("Application shutdown...")
    try:
        get_rabbitmq_publisher().close()
    except Exception as e:
        logger.error(f"Error closing RabbitMQ connection: {e}", exc_info=True)
    logger.info("Application shutdown complete.")


@app.get("/", tags=["Health Check"])
async def read_root():
    """
    Root endpoint for health checks.
    """
    return {"status": "ok", "service": settings.PROJECT_NAME}


# --- Uvicorn Runner ---
if __name__ == "__main__":
    # This block is for direct execution, e.g., `python main.py`
    # In production, you'd typically use a process manager like Gunicorn with Uvicorn workers.
    # Example: gunicorn creativeflow.services.aigeneration.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
    uvicorn.run(app, host="0.0.0.0", port=8000)