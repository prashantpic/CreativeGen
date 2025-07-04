import pika
import json
import logging
import asyncio
from functools import partial

logger = logging.getLogger(__name__)

class RabbitMQPublisher:
    """
    Client for publishing messages (generation jobs) to RabbitMQ.
    
    Uses pika's BlockingConnection and runs publishing in a separate thread
    to avoid blocking the main asyncio event loop. For a fully async solution,
    consider using a library like aio-pika.
    """
    def __init__(self, rabbitmq_url: str):
        self._url = rabbitmq_url
        self._connection = None
        self._channel = None
        self._connect()

    def _connect(self):
        """Establishes a connection and channel to RabbitMQ."""
        try:
            logger.info("Connecting to RabbitMQ...")
            params = pika.URLParameters(self._url)
            self._connection = pika.BlockingConnection(params)
            self._channel = self._connection.channel()
            logger.info("Successfully connected to RabbitMQ.")
        except pika.exceptions.AMQPConnectionError as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}", exc_info=True)
            self._connection = None
            self._channel = None
            raise

    def _ensure_connection(self):
        """Reconnects if the connection is lost."""
        if not self._channel or self._channel.is_closed:
            logger.warning("RabbitMQ connection lost. Attempting to reconnect...")
            self._connect()

    def _publish_sync(self, exchange_name: str, routing_key: str, body: str):
        """The synchronous publishing logic that will run in the thread pool."""
        self._ensure_connection()
        if not self._channel:
            raise ConnectionError("Cannot publish message, RabbitMQ is not connected.")
            
        self._channel.exchange_declare(exchange=exchange_name, exchange_type='direct', durable=True)
        
        self._channel.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=body,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
                content_type='application/json'
            )
        )
        logger.debug(f"Published message to exchange '{exchange_name}' with routing key '{routing_key}'.")

    async def publish_generation_job(self, job_payload: dict, routing_key: str, exchange_name: str):
        """
        Asynchronously publishes a job to RabbitMQ by running the blocking I/O
        in a separate thread.
        
        :param job_payload: A dictionary representing the job.
        :param routing_key: The routing key for the message.
        :param exchange_name: The name of the exchange to publish to.
        """
        loop = asyncio.get_running_loop()
        try:
            body = json.dumps(job_payload, default=str)
            
            # Use partial to pass arguments to the sync function
            sync_publish_with_args = partial(self._publish_sync, exchange_name, routing_key, body)
            
            await loop.run_in_executor(None, sync_publish_with_args)
            
        except TypeError as e:
            logger.error(f"Failed to serialize job payload to JSON: {e}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred during RabbitMQ publishing: {e}", exc_info=True)
            # This allows the service layer to catch and handle the failure
            raise

    def close(self):
        """Closes the connection to RabbitMQ."""
        if self._connection and self._connection.is_open:
            logger.info("Closing RabbitMQ connection.")
            self._connection.close()