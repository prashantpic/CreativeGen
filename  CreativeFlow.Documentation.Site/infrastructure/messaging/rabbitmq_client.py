```python
import asyncio
import logging
from typing import Optional

import aio_pika
from aio_pika.abc import AbstractRobustConnection

logger = logging.getLogger(__name__)


class RabbitMQClient:
    """
    Manages a robust connection to a RabbitMQ broker.
    """
    def __init__(self):
        self.connection: Optional[AbstractRobustConnection] = None

    async def connect(self, url: str):
        """
        Establishes a robust connection to RabbitMQ.
        It will automatically try to reconnect if the connection is lost.
        """
        if self.connection and not self.connection.is_closed:
            logger.warning("RabbitMQ connection already established.")
            return

        try:
            self.connection = await aio_pika.connect_robust(url)
            self.connection.add_close_callback(self._on_close)
            self.connection.add_reconnect_callback(self._on_reconnect)
            logger.info("Successfully connected to RabbitMQ.")
        except asyncio.CancelledError:
            logger.info("RabbitMQ connection attempt cancelled.")
        except Exception:
            logger.exception("Failed to connect to RabbitMQ.")
            raise

    async def close(self):
        """
        Closes the connection to RabbitMQ.
        """
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
            logger.info("RabbitMQ connection closed.")

    async def get_channel(self) -> aio_pika.Channel:
        """
        Retrieves a new channel from the existing connection.
        Raises an exception if the connection is not established.
        """
        if not self.connection or self.connection.is_closed:
            raise ConnectionError("RabbitMQ connection is not available.")
        return await self.connection.channel()

    def _on_close(self, sender, exc):
        logger.warning(f"RabbitMQ connection closed. Exception: {exc}")

    def _on_reconnect(self, sender):
        logger.info("Reconnecting to RabbitMQ...")


# Singleton instance of the RabbitMQ client
rabbitmq_client = RabbitMQClient()
```