import asyncio
import logging
from typing import Callable, Awaitable

import redis.asyncio as aioredis
from redis.exceptions import RedisError

logger = logging.getLogger(__name__)

class PubSubManager:
    """
    Manages Redis Pub/Sub functionalities for broadcasting messages across
    multiple service instances. This is essential for scaling WebSockets,
    ensuring that a message sent from a client connected to one instance
    is broadcast to all clients in the same session, regardless of which
    instance they are connected to.
    """

    def __init__(self, redis_client: aioredis.Redis):
        """
        Initializes the PubSubManager.

        Args:
            redis_client (aioredis.Redis): An asynchronous Redis client instance.
        """
        self.redis_client = redis_client
        self.pubsub = self.redis_client.pubsub()
        self._is_subscribed = False
        self._listener_task: Optional[asyncio.Task] = None

    async def publish_message(self, channel: str, message: str) -> None:
        """
        Publishes a message to a specific Redis channel.

        Args:
            channel (str): The name of the channel to publish to.
            message (str): The message to be sent.
        """
        try:
            await self.redis_client.publish(channel, message)
            logger.debug("Published message to Redis channel '%s'", channel)
        except RedisError as e:
            logger.error(
                "Failed to publish message to Redis channel '%s': %s",
                channel, e, exc_info=True
            )
            # Depending on the application's needs, this might re-raise the exception
            # or just log the error.
            raise

    async def _listener(self, callback: Callable[[str, str], Awaitable[None]]):
        """The background task that listens for messages."""
        logger.info("Redis Pub/Sub listener started.")
        while self._is_subscribed:
            try:
                message = await self.pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                if message and message.get("type") == "message":
                    channel = message['channel'].decode('utf-8')
                    data = message['data'].decode('utf-8')
                    logger.debug("Received message from Redis channel '%s'", channel)
                    # Execute the callback to handle the message
                    await callback(channel, data)
            except asyncio.CancelledError:
                logger.info("Redis Pub/Sub listener task cancelled.")
                break
            except RedisError as e:
                logger.error("Redis Pub/Sub listener error: %s", e, exc_info=True)
                # Implement backoff/retry logic if necessary
                await asyncio.sleep(5)
            except Exception as e:
                logger.error("Unexpected error in Pub/Sub listener: %s", e, exc_info=True)
                await asyncio.sleep(5)
        logger.info("Redis Pub/Sub listener stopped.")


    async def subscribe_to_channel(self, channel: str, callback: Callable[[str, str], Awaitable[None]]):
        """
        Subscribes to a channel and starts a listener task.

        Args:
            channel (str): The channel to subscribe to.
            callback (Callable[[str, str], Awaitable[None]]): An async function that will be
                called with the channel and message data when a message is received.
        """
        if self._is_subscribed:
            # If already subscribed, just add the new channel
            await self.pubsub.subscribe(channel)
        else:
            # First time subscribing, start the listener task
            await self.pubsub.subscribe(channel)
            self._is_subscribed = True
            self._listener_task = asyncio.create_task(self._listener(callback))
            logger.info("Subscribed to Redis channel '%s' and started listener task.", channel)

    async def unsubscribe_from_channel(self, channel: str):
        """
        Unsubscribes from a specific channel.
        """
        try:
            await self.pubsub.unsubscribe(channel)
            logger.info("Unsubscribed from Redis channel '%s'.", channel)
        except RedisError as e:
            logger.error("Failed to unsubscribe from Redis channel '%s': %s", channel, e)


    async def close(self):
        """
        Gracefully shuts down the Pub/Sub manager.
        """
        if self._listener_task and not self._listener_task.done():
            self._is_subscribed = False
            self._listener_task.cancel()
            await self._listener_task
        if self.pubsub:
            await self.pubsub.close()
        logger.info("PubSubManager closed gracefully.")