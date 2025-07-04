import logging
import json
import asyncio
from typing import Dict, Any

import pika
from pika.exceptions import AMQPConnectionError, ChannelClosedByBroker

logger = logging.getLogger(__name__)

class GenerationJobPublishError(Exception):
    """Custom exception for failures in publishing jobs."""
    pass

class RabbitMQPublisher:
    """
    A client for publishing messages (generation jobs) to RabbitMQ.
    
    This implementation uses the blocking `pika` library. In an async application,
    `aio-pika` is a better choice. For simplicity and demonstration, we run blocking
    calls in a separate thread using `asyncio.to_thread`.
    """
    def __init__(self, amqp_url: str, exchange_name: str):
        self._amqp_url = amqp_url
        self._exchange_name = exchange_name
        self._connection: pika.BlockingConnection | None = None
        self._channel: pika.channel.Channel | None = None
        self.is_connected = False

    def _blocking_connect(self):
        """Establishes a blocking connection and channel."""
        logger.info("Attempting to connect to RabbitMQ...")
        try:
            params = pika.URLParameters(self._amqp_url)
            self._connection = pika.BlockingConnection(params)
            self._channel = self._connection.channel()
            self._channel.exchange_declare(
                exchange=self._exchange_name,
                exchange_type='direct',
                durable=True
            )
            self.is_connected = True
            logger.info("RabbitMQ connection successful.")
        except AMQPConnectionError as e:
            self.is_connected = False
            logger.critical(f"Failed to connect to RabbitMQ: {e}", exc_info=True)
            raise

    async def connect(self):
        """Asynchronously establishes the connection."""
        await asyncio.to_thread(self._blocking_connect)

    def _blocking_publish(self, body: Dict[str, Any], routing_key: str):
        """Publishes a message in a blocking manner."""
        if not self._channel or not self.is_connected:
            raise GenerationJobPublishError("Cannot publish message, RabbitMQ channel is not open.")
        
        try:
            self._channel.basic_publish(
                exchange=self._exchange_name,
                routing_key=routing_key,
                body=json.dumps(body, default=str), # Use default=str for UUIDs, datetimes
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
                    content_type='application/json'
                )
            )
            logger.debug(f"Published message to exchange '{self._exchange_name}' with key '{routing_key}'")
        except (ChannelClosedByBroker, AMQPConnectionError) as e:
            logger.error(f"RabbitMQ connection error during publish: {e}", exc_info=True)
            self.is_connected = False
            # You might want to attempt a reconnect here
            raise GenerationJobPublishError(f"RabbitMQ connection failed during publish: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred during RabbitMQ publish: {e}", exc_info=True)
            raise GenerationJobPublishError(f"Unexpected error during publish: {e}")

    async def publish_generation_job(self, job_payload: Dict[str, Any], routing_key: str = None) -> None:
        """
        Asynchronously publishes a generation job payload to RabbitMQ.
        
        :param job_payload: The dictionary payload for the job.
        :param routing_key: The routing key for the message.
        """
        if routing_key is None:
            from creativeflow.services.aigeneration.core.config import settings
            routing_key = settings.RABBITMQ_N8N_JOB_ROUTING_KEY
            
        try:
            await asyncio.to_thread(self._blocking_publish, job_payload, routing_key)
        except Exception as e:
            # The underlying `_blocking_publish` raises GenerationJobPublishError.
            # We just re-raise it.
            raise e from e

    def _blocking_close(self):
        """Closes the connection in a blocking manner."""
        try:
            if self._channel and self._channel.is_open:
                self._channel.close()
            if self._connection and self._connection.is_open:
                self._connection.close()
            logger.info("RabbitMQ connection closed gracefully.")
        except Exception as e:
            logger.error(f"Error closing RabbitMQ connection: {e}", exc_info=True)
        finally:
            self.is_connected = False

    async def close(self):
        """Asynchronously closes the connection."""
        if self.is_connected:
            await asyncio.to_thread(self._blocking_close)