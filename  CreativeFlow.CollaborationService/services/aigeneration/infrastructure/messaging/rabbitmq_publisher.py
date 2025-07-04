import logging
import json
from typing import Optional, Dict, Any

import aio_pika
from aio_pika.abc import AbstractRobustConnection, AbstractChannel

from creativeflow.services.aigeneration.application.exceptions import GenerationJobPublishError

logger = logging.getLogger(__name__)

class RabbitMQPublisher:
    """
    Handles publishing messages (generation jobs) to RabbitMQ.
    Uses aio_pika for asynchronous operations.
    """
    def __init__(self, amqp_url: str, exchange_name: str):
        self._amqp_url = amqp_url
        self._exchange_name = exchange_name
        self._connection: Optional[AbstractRobustConnection] = None
        self._channel: Optional[AbstractChannel] = None

    async def connect(self):
        """Establishes a connection and a channel to RabbitMQ."""
        try:
            self._connection = await aio_pika.connect_robust(self._amqp_url)
            self._channel = await self._connection.channel()
            # Declare the exchange to ensure it exists
            await self._channel.declare_exchange(
                self._exchange_name,
                aio_pika.ExchangeType.DIRECT,
                durable=True
            )
            logger.info("Successfully connected to RabbitMQ and declared exchange.")
        except Exception as e:
            logger.critical(f"Failed to connect to RabbitMQ: {e}", exc_info=True)
            raise GenerationJobPublishError("Could not establish RabbitMQ connection.")

    async def close(self):
        """Closes the RabbitMQ channel and connection gracefully."""
        if self._channel and not self._channel.is_closed:
            await self._channel.close()
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
        logger.info("RabbitMQ connection closed.")

    async def publish_generation_job(self, job_payload: Dict[str, Any], routing_key: str):
        """
        Publishes a generation job to the configured exchange.

        :param job_payload: A dictionary representing the job payload.
        :param routing_key: The routing key for the message.
        """
        if not self._channel or self._channel.is_closed:
            logger.error("Cannot publish message: RabbitMQ channel is not available.")
            raise GenerationJobPublishError("RabbitMQ channel is not open.")
        
        try:
            message_body = json.dumps(job_payload, default=str).encode()
            
            message = aio_pika.Message(
                body=message_body,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT, # Make message durable
                content_type="application/json"
            )

            await self._channel.default_exchange.publish(
                message,
                routing_key=routing_key
            )
            
            logger.info(
                f"Published job for request ID {job_payload.get('generation_request_id')} "
                f"with routing key '{routing_key}'"
            )

        except Exception as e:
            logger.error(
                f"Failed to publish generation job for request ID {job_payload.get('generation_request_id')}: {e}",
                exc_info=True
            )
            raise GenerationJobPublishError(f"Failed to publish message: {e}")