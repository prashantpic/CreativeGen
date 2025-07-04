import logging
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from creativeflow.services.aigeneration.api.v1.endpoints import generation_requests, n8n_callbacks
from creativeflow.services.aigeneration.core.config import settings
from creativeflow.services.aigeneration.core.dependencies import rabbitmq_publisher_instance, http_client
from creativeflow.services.aigeneration.core.error_handlers import register_error_handlers
from creativeflow.services.aigeneration.core.logging_config import setup_logging
from creativeflow.services.aigeneration.infrastructure.database.db_config import init_db

# Setup logging as the first thing
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# --- Event Handlers ---

@app.on_event("startup")
async def startup_event():
    """
    Application startup event.
    Connect to RabbitMQ and initialize database if needed.
    """
    logger.info("Application startup...")
    try:
        await rabbitmq_publisher_instance.connect()
    except Exception as e:
        logger.critical(f"Could not connect to RabbitMQ on startup. The service might not function correctly. Error: {e}")
    # The DB engine connects on-demand, but we can run init_db for dev/testing
    # In a production setup with Alembic, you would not call init_db() here.
    # await init_db()
    logger.info("Application startup complete.")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown event.
    Gracefully close connections.
    """
    logger.info("Application shutdown...")
    await rabbitmq_publisher_instance.close()
    await http_client.aclose()
    logger.info("Application shutdown complete.")

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
register_error_handlers(app)

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
    Root endpoint for basic health checks.
    """
    return {"status": "ok", "service": settings.PROJECT_NAME}


if __name__ == "__main__":
    # Note: This block is for direct execution, not for production deployment with Gunicorn/Uvicorn process manager.
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True, # Reload should be False in production
        log_level=settings.LOG_LEVEL.lower()
    )