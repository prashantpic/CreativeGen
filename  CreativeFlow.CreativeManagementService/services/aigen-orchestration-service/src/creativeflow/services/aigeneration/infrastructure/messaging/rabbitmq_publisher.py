"""
RabbitMQ Publisher for Dispatching Generation Jobs.

This module provides a client for publishing messages (generation jobs) to a
RabbitMQ message broker. It encapsulates the logic for connection management,
channel handling, and publishing persistent messages to ensure reliability.

Note: The SDS specified 'pika'. Pika is a blocking library. To use it in an
asyncio application without blocking the event loop, its operations must be
run in a separate thread. This implementation uses `asyncio.to_thread` for
that purpose. For a new project, `aiopika` would be a more idiomatic choice.
"""

import asyncio
import json
import logging
from typing import Optional

import pika
from pika.exceptions import AMQPConnectionError, ChannelClosedByBroker

logger = logging.getLogger(__name__)

class RabbitMQPublisher:
    """
    A client for publishing messages to RabbitMQ.
    Handles connection and publishing logic in an async-friendly way.
    """

    def __init__(self, amqp_url: str, exchange_name: str):
        self.amqp_url = amqp_url
        self.exchange_name = exchange_name
        self._connection: Optional[pika.BlockingConnection] = None
        self._channel: Optional[pika.channel.Channel] = None
        self._lock = asyncio.Lock()

    @property
    def is_connected(self) -> bool:
        """Check if the connection and channel are active."""
        return self._connection is not None and self._connection.is_open and \
               self._channel is not None and self._channel.is_open

    async def connect(self):
        """
        Establishes a connection to RabbitMQ and declares the exchange.
        This method is thread-safe.
        """
        async with self._lock:
            if self.is_connected:
                logger.info("RabbitMQ connection is already active.")
                return

            logger.info("Connecting to RabbitMQ...")
            try:
                # Run blocking pika connection code in a separate thread
                await asyncio.to_thread(self._blocking_connect)
                logger.info("Successfully connected to RabbitMQ and declared exchange.")
            except AMQPConnectionError as e:
                logger.critical(f"Failed to connect to RabbitMQ: {e}")
                self._connection = None
                self._channel = None
                raise

    def _blocking_connect(self):
        """The synchronous part of the connection logic."""
        params = pika.URLParameters(self.amqp_url)
        self._connection = pika.BlockingConnection(params)
        self._channel = self._connection.channel()
        # Declare a durable exchange to ensure it survives broker restarts
        self._channel.exchange_declare(
            exchange=self.exchange_name,
            exchange_type='direct',
            durable=True
        )

    async def publish_message(self, message_body: str, routing_key: str = "n8n.job.create"):
        """
        Publishes a message to the configured RabbitMQ exchange.
        Ensures the message is persistent.

        Args:
            message_body: The message content, typically a JSON string.
            routing_key: The routing key for the message.
        """
        if not self.is_connected:
            logger.warning("Not connected to RabbitMQ. Attempting to reconnect...")
            await self.connect()

        try:
            # Run blocking pika publish code in a separate thread
            await asyncio.to_thread(
                self._blocking_publish, message_body, routing_key
            )
            logger.debug(f"Successfully published message with routing key '{routing_key}'")
        except (AMQPConnectionError, ChannelClosedByBroker) as e:
            logger.error(f"RabbitMQ connection error during publish: {e}. Attempting to reconnect and retry.")
            await self.close()
            await self.connect()
            # Retry once after reconnecting
            await asyncio.to_thread(
                self._blocking_publish, message_body, routing_key
            )
            logger.info("Successfully published message after reconnecting.")
        except Exception as e:
            logger.error(f"An unexpected error occurred during message publishing: {e}", exc_info=True)
            raise

    def _blocking_publish(self, message_body: str, routing_key: str):
        """The synchronous part of the publishing logic."""
        if not self._channel:
            raise ConnectionError("RabbitMQ channel is not available.")
            
        self._channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=routing_key,
            body=message_body,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
                content_type='application/json'
            )
        )

    async def close(self):
        """Closes the RabbitMQ connection gracefully."""
        async with self._lock:
            if self._connection and self._connection.is_open:
                logger.info("Closing RabbitMQ connection.")
                await asyncio.to_thread(self._connection.close)
            self._connection = None
            self._channel = None