"""
The concrete implementation of the IJobPublisher interface using aio_pika.
It handles publishing generation jobs to a RabbitMQ message broker asynchronously.
"""
import json
import logging
from typing import Any, Dict

import aio_pika
from aio_pika.abc import AbstractRobustConnection

from ...app.interfaces import IJobPublisher
from ...config.settings import settings

logger = logging.getLogger(__name__)


class PikaJobPublisher(IJobPublisher):
    """
    Implements the job publisher interface using aio_pika to send messages
    asynchronously to a RabbitMQ queue.
    """

    def __init__(self, connection: AbstractRobustConnection):
        self._connection = connection
        self._queue_name = settings.GENERATION_JOB_QUEUE

    async def publish_generation_job(self, job_payload: Dict[str, Any]) -> None:
        """
        Serializes the job payload into JSON and publishes a persistent message
        to the configured RabbitMQ queue for n8n to process.
        """
        try:
            # Get a channel from the connection
            async with self._connection.channel() as channel:
                # Declaring queue as durable to survive broker restart
                await channel.declare_queue(
                    self._queue_name,
                    durable=True
                )

                message_body = json.dumps(job_payload).encode()
                message = aio_pika.Message(
                    body=message_body,
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT,  # Make message persistent
                )

                # Publishes a message to the default exchange with a routing key
                # that is the name of the queue.
                await channel.default_exchange.publish(
                    message,
                    routing_key=self._queue_name
                )
                logger.info(
                    f"Successfully published job {job_payload.get('generationId')} to queue '{self._queue_name}'"
                )

        except Exception as e:
            logger.critical(f"Failed to publish job to RabbitMQ: {e}", exc_info=True)
            # Depending on the desired behavior, this could re-raise the exception
            # to cause the parent transaction to fail.
            raise


async def get_pika_connection() -> AbstractRobustConnection:
    """Factory function to create a robust RabbitMQ connection."""
    return await aio_pika.connect_robust(settings.RABBITMQ_URL)