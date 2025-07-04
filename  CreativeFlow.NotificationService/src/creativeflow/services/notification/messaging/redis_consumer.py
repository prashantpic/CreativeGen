"""
Redis Pub/Sub message consumer using the async `redis` library.

This module provides a class to connect to Redis, subscribe to a Pub/Sub
channel, and process messages asynchronously. It is designed to run as an
asyncio task within the main application's event loop.
"""
import asyncio

import redis.asyncio as redis
from redis.exceptions import ConnectionError as RedisConnectionError

from creativeflow.services.notification.config import Settings
from creativeflow.services.notification.messaging.message_handler import MessageHandler
from creativeflow.services.notification.shared.logger import get_logger

logger = get_logger(__name__)


class RedisConsumer:
    """
    Consumes messages from a Redis Pub/Sub channel and processes them.
    """

    def __init__(self, config: Settings, message_handler: MessageHandler):
        """
        Initializes the RedisConsumer.

        Args:
            config: The application settings.
            message_handler: The message handler for processing messages.
        """
        self.config = config
        self.message_handler = message_handler
        self.redis_client = None
        self.pubsub = None
        self._task = None

    async def connect(self):
        """Establishes and verifies a connection to Redis."""
        try:
            logger.info(f"Connecting to Redis at {self.config.REDIS_URL}")
            self.redis_client = redis.from_url(self.config.REDIS_URL, decode_responses=True)
            await self.redis_client.ping()
            logger.info("Redis connection established successfully.")
            return True
        except RedisConnectionError as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self.redis_client = None
            return False

    async def subscribe_and_listen(self, channel_name: str):
        """
        Subscribes to a Redis channel and enters a loop to listen for messages.
        This is an async method intended to be run as a background task.
        """
        if not self.config.ENABLE_REDIS_CONSUMER:
            logger.info("Redis consumer is disabled. Will not start.")
            return

        if not self.redis_client and not await self.connect():
            logger.error("Cannot start listening, Redis connection failed.")
            return

        self.pubsub = self.redis_client.pubsub()
        await self.pubsub.subscribe(channel_name)
        logger.info(f"Subscribed to Redis Pub/Sub channel: '{channel_name}'")

        while True:
            try:
                message = await self.pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                if message and message.get('type') == 'message':
                    logger.debug(f"Received message from Redis channel '{message['channel']}'")
                    try:
                        await self.message_handler.handle_message(message['data'], "Redis Pub/Sub")
                    except Exception as e:
                        logger.error(f"Error handling message from Redis: {e}. Message: {message['data']}")
            except asyncio.CancelledError:
                logger.info("Redis listener task cancelled. Shutting down.")
                break
            except RedisConnectionError as e:
                logger.error(f"Redis connection lost: {e}. Attempting to reconnect...")
                await self.stop_listening()
                await asyncio.sleep(5)
                # Re-enter the loop to attempt reconnection and resubscription
                if await self.connect():
                    self.pubsub = self.redis_client.pubsub()
                    await self.pubsub.subscribe(channel_name)
                    logger.info(f"Re-subscribed to Redis channel: '{channel_name}'")
                else:
                    logger.error("Failed to reconnect to Redis. Listener will not continue.")
                    break
            except Exception as e:
                logger.exception(f"An unexpected error occurred in Redis listener loop: {e}")
                await asyncio.sleep(5)

        await self.stop_listening()

    async def stop_listening(self):
        """Gracefully stops the listener and closes connections."""
        logger.info("Stopping Redis consumer...")
        if self.pubsub:
            try:
                await self.pubsub.unsubscribe()
                await self.pubsub.close()
                self.pubsub = None
                logger.info("Unsubscribed from Redis channels.")
            except Exception as e:
                logger.error(f"Error during Redis pubsub cleanup: {e}")

        if self.redis_client:
            try:
                await self.redis_client.close()
                self.redis_client = None
                logger.info("Redis connection closed.")
            except Exception as e:
                logger.error(f"Error closing Redis client: {e}")