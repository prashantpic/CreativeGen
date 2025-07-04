"""
Entry point for the UserProfile microservice. Initializes and configures
the FastAPI application.
"""
import contextlib
import logging

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .adapters.api.v1.routers import api_v1_router
from .adapters.db.database import create_db_and_tables
from .config import get_settings
from .domain.exceptions import ProfileNotFoundError
from .logging_config import setup_logging


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages application startup and shutdown events.
    """
    settings = get_settings()
    setup_logging(log_level=settings.LOG_LEVEL)
    
    if settings.ENVIRONMENT == "development":
        logging.info("Development environment detected. Creating database tables...")
        await create_db_and_tables()
        logging.info("Database tables created.")

    logging.info("Service starting up...")
    yield
    logging.info("Service shutting down...")


def create_application() -> FastAPI:
    """
    Creates and configures the FastAPI application instance.
    """
    settings = get_settings()
    app = FastAPI(
        title=settings.PROJECT_NAME,
        lifespan=lifespan,
        version="0.1.0",
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, restrict this to specific domains
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routers
    app.include_router(api_v1_router, prefix=settings.API_V1_STR)

    # --- Global Exception Handlers ---
    @app.exception_handler(ProfileNotFoundError)
    async def profile_not_found_exception_handler(
        request: Request, exc: ProfileNotFoundError
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(exc)},
        )

    @app.get("/", tags=["Health Check"])
    async def read_root():
        """A simple health check endpoint."""
        return {"status": "ok", "service": settings.PROJECT_NAME}

    return app


app = create_application()

if __name__ == "__main__":
    # This block is for local development and debugging
    uvicorn.run(
        "creativeflow.services.userprofile.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )