import logging
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .core.logging_config import setup_logging
from .core.error_handlers import add_exception_handlers
from .core.dependencies import rabbitmq_publisher_instance
from .api.v1.endpoints import generation_requests, n8n_callbacks
from .infrastructure.database.db_config import Base, engine

# --- Application Setup ---

# Initialize logging as early as possible
setup_logging()
logger = logging.getLogger(__name__)

# Create FastAPI app instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# --- Middleware ---

# Add CORS middleware if needed (adjust origins as necessary for your frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or a list of specific origins: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Event Handlers ---

@app.on_event("startup")
async def startup_event():
    """
    Application startup logic.
    - Initialize database tables.
    - Connect to RabbitMQ.
    """
    logger.info("Application startup...")
    
    # Initialize database
    try:
        async with engine.begin() as conn:
            # This will create tables if they don't exist.
            # For production, Alembic migrations are preferred.
            # await conn.run_sync(Base.metadata.drop_all) # Use for testing to clear db
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables verified/created.")
    except Exception as e:
        logger.critical(f"Failed to connect to database and create tables: {e}", exc_info=True)
        # Prevent app from starting if DB is down
        raise
        
    # Connect to RabbitMQ
    try:
        await rabbitmq_publisher_instance.connect()
    except Exception as e:
        logger.critical(f"Failed to connect to RabbitMQ on startup: {e}", exc_info=True)
        # Prevent app from starting if RabbitMQ is down
        raise

    logger.info("Application startup complete.")

@app.on_event("shutdown")
async def shutdown_event():
    """

    Application shutdown logic.
    - Gracefully close RabbitMQ connection.
    """
    logger.info("Application shutdown...")
    await rabbitmq_publisher_instance.close()
    logger.info("Application shutdown complete.")


# --- Exception Handlers ---
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
    """Health check endpoint."""
    return {"status": "ok", "service": settings.PROJECT_NAME}


# --- Main Entrypoint for Uvicorn ---
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Set to False in production
    )