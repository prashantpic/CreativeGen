import asyncio
import json
import logging
from typing import Optional

import aio_pika
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel, AbstractRobustExchange
from tenacity import retry, stop_after_attempt, wait_fixed, before_sleep_log

logger = logging.getLogger(__name__)

class RabbitMQPublisher:
    """
    A robust RabbitMQ publisher using aio-pika for asynchronous operations.
    It handles connection and channel management and publishes messages to an exchange.
    Implemented as a singleton to maintain a single connection.
    """
    _instance = None
    _lock = asyncio.Lock()

    def __init__(self, amqp_url: str):
        if not hasattr(self, '_initialized'):
            self.amqp_url = amqp_url
            self.connection: Optional[AbstractRobustConnection] = None
            self.channel: Optional[AbstractRobustChannel] = None
            self._initialized = True

    @classmethod
    def get_instance(cls):
        """Gets the singleton instance."""
        if cls._instance is None:
            raise RuntimeError("RabbitMQPublisher is not initialized. Call initialize() first.")
        return cls._instance

    @classmethod
    async def initialize(cls, amqp_url: str):
        """Initializes the singleton instance and connects to RabbitMQ."""
        async with cls._lock:
            if cls._instance is None:
                cls._instance = cls(amqp_url)
                await cls._instance.connect()

    @classmethod
    async def close(cls):
        """Closes the connection."""
        if cls._instance:
            await cls._instance._close()
            cls._instance = None

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_fixed(3),
        before_sleep=before_sleep_log(logger, logging.WARNING)
    )
    async def connect(self):
        """Establishes a robust connection and channel to RabbitMQ."""
        try:
            self.connection = await aio_pika.connect_robust(self.amqp_url)
            self.channel = await self.connection.channel()
            logger.info("Successfully connected to RabbitMQ.")
        except Exception as e:
            logger.error("Failed to connect to RabbitMQ. Retrying...", exc_info=True)
            raise e

    async def _close(self):
        """Internal method to close the connection and channel."""
        if self.channel and not self.channel.is_closed:
            await self.channel.close()
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
        logger.info("RabbitMQ connection closed.")

    async def publish_generation_job(
        self, job_payload: dict, routing_key: str, exchange_name: str
    ):
        """
        Publishes a generation job payload to a specified exchange.
        
        Args:
            job_payload: The job data as a dictionary.
            routing_key: The routing key for the message.
            exchange_name: The name of the exchange to publish to.
        """
        if not self.connection or self.connection.is_closed:
            logger.error("Cannot publish message: RabbitMQ is not connected.")
            raise ConnectionError("RabbitMQ connection is not available.")

        try:
            exchange = await self.channel.declare_exchange(
                exchange_name, aio_pika.ExchangeType.DIRECT, durable=True
            )
            
            message_body = json.dumps(job_payload, default=str).encode()
            
            message = aio_pika.Message(
                body=message_body,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT, # Make message durable
                content_type="application/json",
            )
            
            await exchange.publish(message, routing_key=routing_key)
            
            logger.info(
                "Published generation job",
                extra={
                    "exchange": exchange_name,
                    "routing_key": routing_key,
                    "request_id": job_payload.get("generation_request_id"),
                },
            )
        except Exception as e:
            logger.critical(
                "Failed to publish message to RabbitMQ",
                extra={"exchange": exchange_name, "routing_key": routing_key},
                exc_info=True
            )
            raise ConnectionError("Failed to publish message to RabbitMQ.") from e