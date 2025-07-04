import logging
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

from creativeflow.service.api.v1.api_router import api_router
from creativeflow.service.core.config import settings
from creativeflow.service.messaging.producer import WebhookEventProducer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Define a lifespan context manager for startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.
    """
    # Startup
    logger.info("Application starting up...")
    app.state.webhook_producer = WebhookEventProducer(
        rabbitmq_url=settings.RABBITMQ_URL,
        exchange_name=settings.WEBHOOK_EXCHANGE_NAME
    )
    try:
        await app.state.webhook_producer.connect()
        logger.info("Webhook producer connected to RabbitMQ.")
    except Exception as e:
        logger.error(f"Failed to connect to RabbitMQ: {e}", exc_info=True)
        # Depending on the desired behavior, you might want to exit or retry
        # For now, we log the error and continue, the producer will be unavailable.

    yield

    # Shutdown
    logger.info("Application shutting down...")
    if hasattr(app.state, 'webhook_producer') and app.state.webhook_producer.is_connected():
        await app.state.webhook_producer.close()
        logger.info("Webhook producer connection closed.")


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Set up CORS middleware
if settings.ALLOWED_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.ALLOWED_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.middleware("http")
async def add_process_time_and_correlation_id(request: Request, call_next) -> Response:
    """
    Middleware to add a correlation ID to each request and log process time.
    """
    start_time = time.time()
    correlation_id = str(uuid.uuid4())
    request.state.correlation_id = correlation_id

    response = await call_next(request)

    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Correlation-ID"] = correlation_id
    logger.info(
        f"request_id={correlation_id} method={request.method} path={request.url.path} status_code={response.status_code} process_time={process_time:.4f}s"
    )
    return response


# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    correlation_id = getattr(request.state, 'correlation_id', 'N/A')
    logger.error(f"Unhandled exception for request {correlation_id}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected internal server error occurred.",
            "correlation_id": correlation_id
        },
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    correlation_id = getattr(request.state, 'correlation_id', 'N/A')
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "correlation_id": correlation_id},
    )


# Include the API router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["Health Check"])
def health_check():
    """
    Simple health check endpoint.
    """
    return {"status": "ok"}