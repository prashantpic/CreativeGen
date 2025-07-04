```python
import json
import logging
from typing import Protocol

import aio_pika

from domain.models.webhook import Webhook
from infrastructure.messaging.rabbitmq_client import RabbitMQClient

logger = logging.getLogger(__name__)


class IWebhookPublisher(Protocol):
    """Interface for publishing webhook events."""

    async def publish_webhook_event(
        self, webhook: Webhook, event_type: str, payload: dict
    ) -> None:
        ...


class WebhookPublisher(IWebhookPublisher):
    """
    Publishes webhook events to a RabbitMQ exchange for asynchronous processing.
    """

    def __init__(
        self,
        rabbitmq_client: RabbitMQClient,
        exchange_name: str,
        routing_key_prefix: str,
    ):
        self.rabbitmq_client = rabbitmq_client
        self.exchange_name = exchange_name
        self.routing_key_prefix = routing_key_prefix

    async def publish_webhook_event(
        self, webhook: Webhook, event_type: str, payload: dict
    ) -> None:
        """
        Constructs and publishes a message for a webhook worker to consume.

        The message contains all information the worker needs to make the HTTP POST
        and sign the payload, if necessary.
        """
        try:
            channel = await self.rabbitmq_client.get_channel()
            exchange = await channel.declare_exchange(
                self.exchange_name, aio_pika.ExchangeType.TOPIC, durable=True
            )

            # This message structure is designed for a separate worker.
            # The worker will be responsible for fetching the secret using the webhook.id
            # and performing the HMAC signing before sending the HTTP request.
            message_body = {
                "webhook_id": str(webhook.id),
                "target_url": str(webhook.target_url),
                "event_type": event_type,
                "raw_payload": payload,
                "signature_secret_ref": str(webhook.id) if webhook.hashed_secret else None,
            }
            
            routing_key = f"{self.routing_key_prefix}.{event_type}.{webhook.user_id}"

            message = aio_pika.Message(
                body=json.dumps(message_body).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                content_type="application/json",
            )
            
            await exchange.publish(message, routing_key=routing_key)
            logger.info(
                f"Published webhook event '{event_type}' for webhook {webhook.id} "
                f"with routing key '{routing_key}'"
            )

        except ConnectionError as e:
            logger.error(f"Failed to publish webhook event due to connection error: {e}")
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while publishing webhook event for {webhook.id}: {e}",
                exc_info=True
            )
```