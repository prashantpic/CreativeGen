import logging
from typing import Optional

import aio_pika
from aio_pika.abc import AbstractRobustConnection

logger = logging.getLogger(__name__)


class RabbitMQClient:
    """
    Manages the connection and channel to the RabbitMQ broker.
    """

    def __init__(self, amqp_url: str):
        """
        Initializes the RabbitMQ client.

        Args:
            amqp_url: The connection URL for the RabbitMQ server.
        """
        self.amqp_url = amqp_url
        self.connection: Optional[AbstractRobustConnection] = None

    async def connect(self):
        """
        Establishes a robust connection to RabbitMQ.
        This should be called on application startup.
        """
        if self.connection and not self.connection.is_closed:
            logger.info("RabbitMQ connection already established.")
            return

        try:
            self.connection = await aio_pika.connect_robust(self.amqp_url)
            self.connection.add_close_callback(self._on_connection_close)
            self.connection.add_reconnect_callback(self._on_connection_reconnect)
            logger.info("Successfully connected to RabbitMQ.")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    async def close(self):
        """
        Closes the connection to RabbitMQ.
        This should be called on application shutdown.
        """
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
            logger.info("RabbitMQ connection closed.")

    async def get_channel(self) -> aio_pika.Channel:
        """
        Provides a channel for publishing or consuming messages.

        Returns:
            An aio_pika Channel object.

        Raises:
            ConnectionError: if the connection is not established.
        """
        if not self.connection or self.connection.is_closed:
            logger.error("Attempted to get channel but RabbitMQ is not connected.")
            raise ConnectionError("RabbitMQ connection not available.")
        return await self.connection.channel()

    def _on_connection_close(self, sender, exc):
        logger.warning(f"RabbitMQ connection closed. Exception: {exc}")

    def _on_connection_reconnect(self, sender):
        logger.info("Reconnecting to RabbitMQ...")