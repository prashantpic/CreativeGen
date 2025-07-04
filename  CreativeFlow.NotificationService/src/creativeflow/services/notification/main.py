"""
Main application entry point for the CreativeFlow Notification Service.

This script initializes the FastAPI application, sets up all necessary components
like service managers and message consumers, and defines application lifecycle
events for startup and shutdown.
"""
import asyncio
import threading

from fastapi import FastAPI, Request

from creativeflow.services.notification.api import websocket_endpoints
from creativeflow.services.notification.channels.push.apns_client import APNSClient
from creativeflow.services.notification.channels.push.fcm_client import FCMClient
from creativeflow.services.notification.config import Settings, get_settings
from creativeflow.services.notification.core.notification_manager import NotificationManager
from creativeflow.services.notification.core.push_notification_service import PushNotificationService
from creativeflow.services.notification.core.websocket_manager import WebSocketManager
from creativeflow.services.notification.messaging.message_handler import MessageHandler
from creativeflow.services.notification.messaging.rabbitmq_consumer import RabbitMQConsumer
from creativeflow.services.notification.messaging.redis_consumer import RedisConsumer
from creativeflow.services.notification.shared.logger import get_logger

# Initialize logger
logger = get_logger(__name__, level=get_settings().LOG_LEVEL)

# FastAPI application instance
app = FastAPI(
    title="CreativeFlow Notification Service",
    description="Manages and delivers real-time updates and push notifications.",
    version="0.1.0"
)


@app.on_event("startup")
async def startup_event():
    """
    Application startup logic.
    Initializes and starts all required background services and consumers.
    """
    logger.info("Starting CreativeFlow Notification Service...")
    settings: Settings = get_settings()
    app.state.settings = settings

    # --- Dependency Injection Setup ---
    # The order of instantiation matters here.
    logger.info("Initializing service components...")
    
    # WebSocket Manager is already instantiated at the module level in its file.
    # We can attach it to the app state for consistency if needed, but it's not required by other components here.
    app.state.websocket_manager = websocket_endpoints.websocket_manager

    # Push Notification Channels
    apns_client = APNSClient(config=settings)
    fcm_client = FCMClient(config=settings)
    
    # Core Services
    push_service = PushNotificationService(apns_client, fcm_client, settings)
    notification_manager = NotificationManager(app.state.websocket_manager, push_service, settings)
    
    # Messaging Layer
    message_handler = MessageHandler(notification_manager)
    logger.info("Service components initialized.")

    # --- Start Message Consumers ---
    # RabbitMQ Consumer (runs in a separate thread)
    if settings.ENABLE_RABBITMQ_CONSUMER:
        logger.info("Starting RabbitMQ consumer...")
        rabbitmq_consumer = RabbitMQConsumer(settings, message_handler)
        app.state.rabbitmq_consumer = rabbitmq_consumer
        consumer_thread = threading.Thread(
            target=rabbitmq_consumer.start_consuming,
            args=(settings.RABBITMQ_QUEUE_NAME_AI_UPDATES,),
            daemon=True
        )
        consumer_thread.start()
        app.state.rabbitmq_thread = consumer_thread

    # Redis Consumer (runs as an asyncio task)
    if settings.ENABLE_REDIS_CONSUMER:
        logger.info("Starting Redis consumer...")
        redis_consumer = RedisConsumer(settings, message_handler)
        await redis_consumer.connect()
        app.state.redis_consumer = redis_consumer
        redis_task = asyncio.create_task(
            redis_consumer.subscribe_and_listen(settings.REDIS_PUBSUB_CHANNEL_NAME)
        )
        app.state.redis_task = redis_task

    logger.info("CreativeFlow Notification Service has started successfully.")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown logic.
    Gracefully stops all running background tasks and consumers.
    """
    logger.info("Shutting down CreativeFlow Notification Service...")

    # Stop RabbitMQ Consumer
    if hasattr(app.state, 'rabbitmq_consumer'):
        logger.info("Stopping RabbitMQ consumer...")
        app.state.rabbitmq_consumer.stop_consuming()
        # Wait for the thread to finish
        if hasattr(app.state, 'rabbitmq_thread'):
            app.state.rabbitmq_thread.join(timeout=5)
        logger.info("RabbitMQ consumer stopped.")

    # Stop Redis Consumer
    if hasattr(app.state, 'redis_task'):
        logger.info("Stopping Redis consumer...")
        app.state.redis_task.cancel()
        try:
            await app.state.redis_task
        except asyncio.CancelledError:
            logger.info("Redis consumer task successfully cancelled.")
        # Ensure final cleanup is called
        if hasattr(app.state, 'redis_consumer'):
            await app.state.redis_consumer.stop_listening()

    logger.info("CreativeFlow Notification Service has shut down gracefully.")


# Include API routers
app.include_router(websocket_endpoints.router, tags=["WebSockets"])


# Health Check Endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Simple health check endpoint to verify the service is running.
    """
    return {"status": "ok"}