# -*- coding: utf-8 -*-
"""
Publishes webhook events to RabbitMQ for asynchronous processing and delivery.
"""
import json
import logging
from typing import Any, Dict

import aio_pika

from domain.models.webhook import Webhook
from domain.repositories.webhook_repository import IWebhookPublisher
from infrastructure.messaging.rabbitmq_client import RabbitMQClient

logger = logging.getLogger(__name__)


class WebhookPublisher(IWebhookPublisher):
    """
    Sends webhook event data to a RabbitMQ exchange for asynchronous processing.
    """

    def __init__(
        self,
        rabbitmq_client: RabbitMQClient,
        exchange_name: str,
        routing_key_prefix: str,
    ):
        """
        Initializes the WebhookPublisher.

        :param rabbitmq_client: An instance of RabbitMQClient for connection handling.
        :param exchange_name: The name of the topic exchange to publish to.
        :param routing_key_prefix: The prefix for routing keys (e.g., 'webhook.event').
        """
        self.rabbitmq_client = rabbitmq_client
        self.exchange_name = exchange_name
        self.routing_key_prefix = routing_key_prefix

    async def publish_webhook_event(
        self, webhook: Webhook, event_type: str, payload: Dict[str, Any]
    ) -> None:
        """
        Publishes a webhook event to the message queue.

        This method constructs a message for a separate worker to consume. The
        worker will be responsible for making the HTTP POST request to the target
        URL and signing the payload if a secret is configured.

        :param webhook: The Webhook domain model object.
        :param event_type: The specific event type string (e.g., 'generation.completed').
        :param payload: The JSON-serializable dictionary payload for the event.
        """
        try:
            channel = await self.rabbitmq_client.get_channel()

            # Declare a durable topic exchange
            exchange = await channel.declare_exchange(
                self.exchange_name, aio_pika.ExchangeType.TOPIC, durable=True
            )

            # Message for the worker, containing all info needed for processing
            message_body = {
                "webhook_id": str(webhook.id),
                "target_url": str(webhook.target_url),
                "raw_payload": json.dumps(payload),
                "event_type": event_type,
                # The worker uses this reference to securely retrieve the secret
                # (e.g., from DB or Vault) for signing the payload.
                "signature_secret_ref": str(webhook.id)
                if webhook.hashed_secret
                else None,
            }

            # e.g., 'webhook.event.generation.completed.user_uuid'
            routing_key = (
                f"{self.routing_key_prefix}.{event_type}.{str(webhook.user_id)}"
            )

            message = aio_pika.Message(
                body=json.dumps(message_body).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                content_type="application/json",
            )

            await exchange.publish(message, routing_key=routing_key)

            logger.info(
                "Published webhook event '%s' for webhook ID %s to exchange '%s' with routing key '%s'.",
                event_type,
                webhook.id,
                self.exchange_name,
                routing_key,
            )

        except Exception as e:
            logger.error(
                "Failed to publish webhook event for webhook ID %s: %s",
                webhook.id,
                e,
                exc_info=True,
            )
            # Depending on requirements, could raise this exception to be handled
            # by the calling service, or just log and continue.
            raise