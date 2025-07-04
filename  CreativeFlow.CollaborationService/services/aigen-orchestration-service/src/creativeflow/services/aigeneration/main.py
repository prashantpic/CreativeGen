import logging
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from creativeflow.services.aigeneration.core.config import settings
from creativeflow.services.aigeneration.core.logging_config import setup_logging
from creativeflow.services.aigeneration.core.error_handlers import setup_error_handlers
from creativeflow.services.aigeneration.infrastructure.database.db_config import init_db
from creativeflow.services.aigeneration.api.v1.endpoints import generation_requests, n8n_callbacks

# Setup logging as early as possible
setup_logging()
logger = logging.getLogger(__name__)

# Create FastAPI app instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    version="1.0.0"
)

# --- Middleware ---
# Configure CORS (Cross-Origin Resource Sharing)
# In a real production environment, this should be more restrictive.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# --- Error Handlers ---
setup_error_handlers(app)

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

# --- Startup and Shutdown Events ---
@app.on_event("startup")
async def startup_event():
    """
    Actions to perform on application startup.
    - Initialize database tables (for dev/testing, migrations for prod)
    """
    logger.info("Application startup...")
    # For dev/testing. In prod, migrations (e.g., Alembic) handle this.
    await init_db()
    logger.info("Application startup complete.")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Actions to perform on application shutdown.
    - Gracefully close connections
    """
    logger.info("Application shutdown...")
    # Add any explicit connection closing logic here if needed,
    # e.g., for a singleton HTTP client or database engine.
    logger.info("Application shutdown complete.")


@app.get("/", tags=["Health Check"])
def read_root():
    """
    Root endpoint for health checks.
    """
    return {"status": "ok", "service": settings.PROJECT_NAME}


if __name__ == "__main__":
    # This block is for running the app directly for development.
    # In production, a process manager like Gunicorn would be used with Uvicorn workers.
    logger.info(f"Starting {settings.PROJECT_NAME}...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level=settings.LOG_LEVEL.lower()
    )