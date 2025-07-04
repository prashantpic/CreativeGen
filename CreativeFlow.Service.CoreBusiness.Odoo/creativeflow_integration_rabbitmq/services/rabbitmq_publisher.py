import pika
import json
import logging
from odoo import api, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class RabbitMQPublisher(models.AbstractModel):
    _name = 'rabbitmq.publisher'
    _description = 'RabbitMQ Publisher Service'

    def _get_connection_params(self):
        """
        Retrieves RabbitMQ connection parameters from Odoo system parameters.
        """
        ICP = self.env['ir.config_parameter'].sudo()
        host = ICP.get_param('rabbitmq.host', 'localhost')
        port = int(ICP.get_param('rabbitmq.port', 5672))
        user = ICP.get_param('rabbitmq.user', 'guest')
        password = ICP.get_param('rabbitmq.password', 'guest')

        credentials = pika.PlainCredentials(user, password)
        return pika.ConnectionParameters(host=host, port=port, credentials=credentials)

    def publish_generation_job(self, job_payload: dict):
        """
        Publishes a creative generation job to a durable topic exchange.

        :param job_payload: A dictionary containing the job details.
        """
        connection = None
        try:
            connection_params = self._get_connection_params()
            connection = pika.BlockingConnection(connection_params)
            channel = connection.channel()

            exchange_name = 'ai_exchange'
            routing_key = 'generation.create'
            
            # Ensure the exchange is durable so it survives broker restarts
            channel.exchange_declare(
                exchange=exchange_name,
                exchange_type='topic',
                durable=True
            )

            message_body = json.dumps(job_payload)

            # Publish the message with persistent delivery mode
            channel.basic_publish(
                exchange=exchange_name,
                routing_key=routing_key,
                body=message_body,
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
                    content_type='application/json',
                )
            )
            _logger.info(
                "Successfully published message to exchange '%s' with routing key '%s'. Payload: %s",
                exchange_name, routing_key, job_payload
            )

        except pika.exceptions.AMQPConnectionError as e:
            _logger.exception(
                "Failed to connect to RabbitMQ. Please check connection parameters. Error: %s", e
            )
            raise UserError(_("Could not queue the generation job. The processing service is currently unavailable. Please try again later."))
        except Exception as e:
            _logger.exception(
                "An unexpected error occurred while publishing to RabbitMQ. Payload: %s. Error: %s",
                job_payload, e
            )
            raise UserError(_("An unexpected error occurred while queueing the generation job."))
        finally:
            if connection and connection.is_open:
                connection.close()