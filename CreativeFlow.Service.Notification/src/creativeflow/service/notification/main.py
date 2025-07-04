import asyncio
import logging

from fastapi import FastAPI

from .core.config import get_settings
from .shared.logging import setup_logging

from .channels.websocket.manager import ConnectionManager
from .channels.websocket.channel import WebSocketChannel
from .channels.push.providers.apns import APNSProvider
from .channels.push.providers.fcm import FCMProvider
from .channels.push.channel import PushNotificationChannel
from .core.dispatcher import NotificationDispatcher
from .entrypoints.consumers import RabbitMQConsumer
from .entrypoints.api import create_api_router

# Configure logging as early as possible
settings = get_settings()
setup_logging(settings.LOG_LEVEL)

logger = logging.getLogger(__name__)

# Create the FastAPI application instance
app = FastAPI(
    title="CreativeFlow Notification Service",
    version="1.0.0",
    description="Delivers real-time and push notifications to users.",
)

@app.on_event("startup")
async def startup_event():
    """
    Application startup lifecycle event.
    Initializes and starts all necessary components and background tasks.
    """
    logger.info("Application startup...")

    # --- Dependency Injection Setup ---
    # 1. Instantiate managers and providers (singletons)
    connection_manager = ConnectionManager()
    apns_provider = APNSProvider(settings)
    fcm_provider = FCMProvider(settings)

    # 2. Instantiate channels with their dependencies
    websocket_channel = WebSocketChannel(connection_manager)
    push_channel = PushNotificationChannel(apns_provider, fcm_provider)

    # 3. Instantiate the core dispatcher
    dispatcher = NotificationDispatcher(websocket_channel, push_channel)

    # 4. Instantiate the message consumer
    consumer = RabbitMQConsumer(
        amqp_url=settings.RABBITMQ_URL,
        queue_name=settings.NOTIFICATION_QUEUE_NAME,
        dispatcher=dispatcher
    )

    # --- Background Task ---
    # Start the RabbitMQ consumer in a background task
    consumer_task = asyncio.create_task(consumer.run())
    
    # Store instances on app.state to be accessible elsewhere if needed,
    # especially for graceful shutdown.
    app.state.consumer = consumer
    app.state.consumer_task = consumer_task

    # --- API Router ---
    # Create and include the API router, injecting the connection manager
    api_router = create_api_router(connection_manager)
    app.include_router(api_router)

    logger.info("Application startup complete.")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown lifecycle event.
    Gracefully stops background tasks and closes connections.
    """
    logger.info("Application shutdown...")
    
    if hasattr(app.state, "consumer_task") and app.state.consumer_task:
        # Gracefully stop the RabbitMQ consumer
        logger.info("Stopping RabbitMQ consumer...")
        app.state.consumer_task.cancel()
        try:
            await app.state.consumer_task
        except asyncio.CancelledError:
            logger.info("Consumer task successfully cancelled.")
    
    if hasattr(app.state, "consumer") and app.state.consumer:
        await app.state.consumer.stop()
        
    # Add shutdown logic for push provider clients if they have persistent connections
    # (e.g., apns_provider.close(), fcm_provider.close())
    
    logger.info("Application shutdown complete.")