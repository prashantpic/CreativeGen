import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1 import api_v1_router
from .core.config import settings
from .infrastructure.odoo_client import OdooClient
from .dependencies import get_odoo_client

# Configure logging based on the settings
logging.basicConfig(level=settings.LOG_LEVEL.upper())
logger = logging.getLogger(__name__)

# Create the FastAPI application instance
app = FastAPI(
    title="CreativeFlow Subscription & Billing Adapter Service",
    description="This service acts as an adapter layer between the CreativeFlow platform and the Odoo ERP system for all subscription, billing, and credit management functionalities.",
    version="1.0.0",
    # Add other OpenAPI metadata if needed
)

# --- Middleware ---
# Configure CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend domain(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Event Handlers ---

@app.on_event("startup")
async def startup_event():
    """
    Actions to perform on application startup.
    e.g., initialize database connections, check Odoo connectivity.
    """
    logger.info("Subscription & Billing Adapter Service is starting up...")
    try:
        # Eagerly initialize the Odoo client to check connectivity on startup
        odoo_client: OdooClient = get_odoo_client(settings)
        odoo_client._ensure_connection()
        logger.info("Odoo connection successful.")
    except Exception as e:
        logger.critical(f"CRITICAL: Could not connect to Odoo on startup. Service may be unhealthy. Error: {e}", exc_info=True)
    logger.info("Startup complete.")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Actions to perform on application shutdown.
    e.g., clean up resources, close connections.
    """
    logger.info("Subscription & Billing Adapter Service is shutting down...")
    # Cleanup logic can go here if needed.
    # Connections managed by `lru_cache` don't require explicit cleanup.

# --- API Routers ---
# Include the main router for API version 1
app.include_router(api_v1_router)

# --- Root and Health Check Endpoints ---

@app.get("/", tags=["Health"])
async def read_root():
    """A simple root endpoint to confirm the service is running."""
    return {"message": "Welcome to the CreativeFlow Subscription & Billing Adapter Service"}

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for load balancers and orchestration platforms.
    Can be expanded to check connectivity to Odoo and the database.
    """
    # A more advanced health check could be implemented here
    # For now, if the app is running, it's considered healthy.
    return {"status": "healthy"}