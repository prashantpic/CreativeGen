# Configuration: RabbitMQ Integration

This document details the configuration required for n8n to connect and interact with the RabbitMQ message broker, which is central to the event-driven architecture of the CreativeFlow AI platform.

## Connection Parameters

The connection to RabbitMQ can be configured using a single URI or individual parameters. Using a URI is generally preferred. These should be set as environment variables for the n8n instance.

*   **`RABBITMQ_URI`** (Recommended)
    *   **Description**: A single connection string that includes all necessary connection details.
    *   **Format**: `amqp://<user>:<password>@<host>:<port>/<vhost>`
    *   **Example**: `amqp://n8n_user:SuperSecretPassword@rabbitmq.creativeflow.svc.cluster.local:5672/creativeflow_vhost`

*   **Individual Parameters** (Alternative if the n8n RabbitMQ node/credential supports it)
    *   `RABBITMQ_HOST`: The hostname of the RabbitMQ server.
    *   `RABBITMQ_PORT`: The port (e.g., `5672` for AMQP, `5671` for AMQPS).
    *   `RABBITMQ_USER`: The username for the connection.
    *   `RABBITMQ_PASSWORD`: The password for the connection.
    *   `RABBITMQ_VHOST`: The virtual host to use.

Within the n8n UI, these parameters will be used to create a "RabbitMQ Credentials" entry.

## Queues and Exchanges

n8n interacts with specific queues and exchanges for consuming jobs and publishing results.

### Job Consumption

*   **Queue Name**: `creative_generation_queue`
    *   **Purpose**: The main queue where the `AI Generation Orchestration Service` publishes job requests.
    *   **n8n Node**: `RabbitMQ Trigger`
    *   **Configuration**: The trigger node in `CreativeGeneration_Main.workflow.json` must be configured to listen to this queue.

### Result & Notification Publishing

n8n publishes messages to exchanges, which then route them to the appropriate queues for downstream services. This provides flexibility.

*   **Notification Service Exchange**
    *   **Exchange Name**: `notification_service_exchange` (or defined by `NOTIFICATION_SERVICE_RABBITMQ_EXCHANGE` env var)
    *   **Type**: `topic` (recommended for routing flexibility)
    *   **Purpose**: To send status updates to the `Notification Service`.
    *   **Routing Keys used by n8n**:
        *   `notifications.creative.completed`
        *   `notifications.creative.failed`
        *   `notifications.creative.content_rejected`
    *   **Queue Binding (to be configured on RabbitMQ)**: `notification_service_queue_creative_updates` should be bound to this exchange with the routing key `notifications.creative.*`.

*   **Odoo Updates Exchange**
    *   **Exchange Name**: `odoo_updates_exchange` (or defined by `ODOO_UPDATES_RABBITMQ_EXCHANGE` env var)
    *   **Type**: `topic` (recommended)
    *   **Purpose**: To send final job status and billing-related information to the Odoo backend.
    *   **Routing Keys used by n8n**:
        *   `odoo.creative.status.completed`
        *   `odoo.creative.status.failed`
        *   `odoo.creative.status.content_rejected`
    *   **Queue Binding (to be configured on RabbitMQ)**: `odoo_updates_queue_creative_status` should be bound to this exchange with the routing key `odoo.creative.status.*`.

*   **Admin Alerts Queue**
    *   **Queue Name**: `admin_alerts_queue`
    *   **Purpose**: The `Utility_ErrorHandling.workflow.json` publishes critical, non-user-facing system errors here for operational monitoring and alerting.
    *   **n8n Node**: `RabbitMQ Produce`

## Connection Options

*   **SSL/TLS**: For production environments, connections should be secured using TLS. This typically involves using the `amqps` protocol in the URI and may require mounting CA certificates into the n8n container.
*   **Heartbeat**: A reasonable heartbeat interval should be configured to prevent connections from being closed by firewalls during periods of inactivity. This is often handled by the client library.