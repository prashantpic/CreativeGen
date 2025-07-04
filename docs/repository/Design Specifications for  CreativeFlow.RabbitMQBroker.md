# Software Design Specification: CreativeFlow.RabbitMQBroker

## 1. Introduction

This document outlines the software design specification for the `CreativeFlow.RabbitMQBroker` repository. This repository is responsible for the configuration, management scripts, and operational definitions of the RabbitMQ message broker cluster used within the CreativeFlow AI platform.

RabbitMQ serves as the central nervous system for asynchronous communication, decoupling services and managing workflows between critical components like the Odoo backend, the n8n workflow engine, AI generation services, and the notification service. The design prioritizes reliability, high availability, and manageability of the messaging infrastructure.

**Key Responsibilities:**
*   Define RabbitMQ server configurations (core, advanced).
*   Provide declarative definitions for production and staging environments (vhosts, users, permissions, queues, exchanges, policies).
*   Offer automation scripts for cluster management, user/permission setup, topology declaration, policy application, and metrics export.
*   Ensure adherence to non-functional requirements related to asynchronous processing, reliability, and infrastructure specifications.

**Technology Stack:**
*   RabbitMQ Server: 3.13.2 (or latest stable at deployment)
*   Erlang: 26.2.5 (compatible with RabbitMQ version)
*   Shell: Bash 5.2.15 (for simple control scripts)
*   Python: 3.11.9 (for more complex management and API interaction scripts)
    *   Libraries: `requests` (for HTTP API), `pika` (for AMQP), `PyYAML` (for config parsing)

## 2. Core Server Configuration

The RabbitMQ server nodes will be configured using two primary files: `rabbitmq.conf` for common settings and `advanced.config` for Erlang-term specific settings.

### 2.1. `rabbitmq.conf`

This file defines fundamental operational parameters.

*   **File Path:** `src/config/rabbitmq.conf`
*   **Purpose:** Main server configuration.
*   **Key Settings:**
    *   **Network Listeners:**
        *   `listeners.tcp.default = 5672` (Standard AMQP port)
        *   `management.tcp.port = 15672` (Management Plugin HTTP API)
        *   `management.ssl.port = 15671` (If SSL is enabled for Management Plugin)
        *   `listeners.ssl.default = 5671` (If SSL is enabled for AMQP)
    *   **Default User (Initial Setup Only):**
        *   `default_user = creativeflow_admin_initial`
        *   `default_pass = <secure_generated_password_to_be_changed_post_setup>`
        *   *Note: This user should be reconfigured or removed and application-specific users created post-initialization using `manage_users.py`.*
    *   **Resource Limits (aligned with DEP-001):**
        *   `disk_free_limit.relative = 1.5` (Disk free space watermark relative to total RAM)
        *   `vm_memory_high_watermark.relative = 0.6` (Memory high watermark at 60% of total RAM, default 0.4)
        *   `file_handle_open_limit = 65536` (Ensure OS ulimits are also set accordingly)
    *   **Logging:**
        *   `log.file.level = info` (Configurable per environment via Ansible: `debug` for dev/staging, `info` or `warning` for prod)
        *   `log.file = /var/log/rabbitmq/rabbit@${HOSTNAME}.log`
        *   `log.dir = /var/log/rabbitmq`
    *   **Clustering:**
        *   `cluster_formation.peer_discovery_backend = rabbit_peer_discovery_classic_config` (Or `rabbit_peer_discovery_dns` if using DNS for discovery)
        *   `cluster_formation.classic_config.nodes.1 = rabbit@node1_hostname`
        *   `cluster_formation.classic_config.nodes.2 = rabbit@node2_hostname`
        *   `cluster_formation.classic_config.nodes.3 = rabbit@node3_hostname` (List all nodes in the cluster)
    *   **Management Plugin:**
        *   `management.load_definitions = /etc/rabbitmq/definitions/production_definitions.json` (Path will be set by Ansible deployment)
        *   `management.sample_retention_policies.global = 3600000` (1 hour)
        *   `management.sample_retention_policies.basic = 3600000` (1 hour)
        *   `management.sample_retention_policies.detailed = 600000` (10 minutes)

### 2.2. `advanced.config`

This file uses Erlang terms for settings not available in `rabbitmq.conf`.

*   **File Path:** `src/config/advanced.config`
*   **Purpose:** Advanced or less common configuration.
*   **Key Settings (Examples):**
    *   **Kernel Parameters:**
        erlang
        [
          {kernel, [
            {inet_default_connect_options, [{nodelay, true}]},
            {inet_default_listen_options, [{nodelay, true}]}
          ]},
          {rabbit, [
            {tcp_listen_options, [{backlog, 2048}, {nodelay, true}, {linger, {true, 0}}, {exit_on_close, false}]},
            {delegate_count, 64} % Number of ETS tables for queue state
          ]}
        ].
        
    *   **SSL/TLS (if enabled for AMQP/Management):**
        erlang
        % Example for enabling SSL on default AMQP listener
        % {rabbit, [
        %   {ssl_listeners, [5671]},
        %   {ssl_options, [
        %     {cacertfile, "/path/to/ca_certificate.pem"},
        %     {certfile, "/path/to/server_certificate.pem"},
        %     {keyfile, "/path/to/server_key.pem"},
        %     {verify, verify_peer},
        %     {fail_if_no_peer_cert, false} % Or true for stricter client cert auth
        %   ]}
        % ]},
        % Example for enabling SSL on Management Plugin
        % {rabbitmq_management, [
        %   {listener, [{port, 15671},
        %               {ssl, true},
        %               {ssl_opts, [
        %                 {cacertfile, "/path/to/ca_certificate.pem"},
        %                 {certfile, "/path/to/server_certificate.pem"},
        %                 {keyfile, "/path/to/server_key.pem"}
        %               ]}
        %              ]}
        % ]}
        
        *Note: SSL paths and options will be managed by Ansible and secure secret distribution.*

## 3. Virtual Hosts, Users, and Permissions

These will be declaratively defined in `production_definitions.json` and `staging_definitions.json` and can also be managed by `manage_users.py`.

### 3.1. Virtual Hosts

*   `/creativeflow_prod`: For all production traffic.
*   `/creativeflow_staging`: For all staging environment traffic.
*   `/`: Default vhost, usage should be restricted or removed for production.

### 3.2. Users and Roles

The `manage_users.py` script will be used to create and manage these users. Passwords should be strong and managed via secure mechanisms (e.g., HashiCorp Vault, then provided to the script).

| User Role                     | Username (Example)        | VHost Access          | Permissions Example (Configure, Write, Read regexes)             | Notes                                                                 |
| :---------------------------- | :------------------------ | :-------------------- | :--------------------------------------------------------------- | :-------------------------------------------------------------------- |
| Odoo Service                  | `odoo_svc`                | `/creativeflow_prod`  | C: `^odoo\.`, W: `^odoo\.`, R: `^n8n\.results\..*\|odoo\..*`      | Publishes Odoo events, consumes n8n results.                          |
| n8n Worker                    | `n8n_worker`              | `/creativeflow_prod`  | C: `^n8n\.`, W: `^n8n\.results\..*`, R: `^ai\.jobs\..*\|odoo\.events\..*` | Consumes AI jobs & Odoo events, publishes results, internal tasks.  |
| AI Service (Internal/Generic) | `ai_svc_internal`         | `/creativeflow_prod`  | C: `^ai\.`, W: `^ai\.results\..*`, R: `^ai\.models\..*`           | For internal AI models interacting with queues.                     |
| Notification Service          | `notification_svc`        | `/creativeflow_prod`  | C: `^notifications\.`, W: `^notifications\.`, R: `^notifications\..*`   | Consumes events, publishes (if needed for direct client responses). |
| API Gateway (if publishing)   | `apigw_publisher`         | `/creativeflow_prod`  | W: `^ai\.jobs\.pending`                                           | If API Gateway directly publishes certain initial requests.           |
| Monitoring Agent              | `monitoring_agent`        | `/` (or specific vhost) | C: `^amq\.gen.*`, W: ``, R: `.*`                                  | Read-only access for metrics.                                         |
| Admin User                    | `rabbitmq_admin_app`      | `/creativeflow_prod`  | C: `.*`, W: `.*`, R: `.*` (Administrator tag)                   | For application-level administrative tasks via scripts.               |

*Staging environment will have similar users, potentially with `_staging` suffix or different passwords.*

### 3.3. Permissions

Permissions will be granularly assigned using `manage_users.py` or defined in the `_definitions.json` files.
*   Producers only get write permissions to specific exchanges/queues.
*   Consumers only get read permissions from specific queues.
*   Configure permissions (`C`) are typically restricted.

## 4. Exchanges, Queues, and Bindings

These will be defined in the input configuration for `declare_entities.py` and reflected in `production_definitions.json` / `staging_definitions.json`.

### 4.1. Exchanges

| Name                      | Type   | VHost                | Durability | Auto-delete | Arguments         | Purpose                                                                                             |
| :------------------------ | :----- | :------------------- | :--------- | :---------- | :---------------- | :-------------------------------------------------------------------------------------------------- |
| `ex.creativeflow.direct`  | direct | `/creativeflow_prod` | true       | false       | `{}`              | For direct routing of commands or specific tasks.                                                   |
| `ex.creativeflow.topic`   | topic  | `/creativeflow_prod` | true       | false       | `{}`              | For event-based communication, flexible routing based on topics.                                    |
| `ex.creativeflow.fanout`  | fanout | `/creativeflow_prod` | true       | false       | `{}`              | For broadcasting messages to multiple consumers (e.g., system-wide notifications).                |
| `ex.dead_letter`          | direct | `/creativeflow_prod` | true       | false       | `{}`              | Central Dead Letter Exchange.                                                                       |
| *(Staging equivalents with `/creativeflow_staging` vhost)* |        |                      |            |             |                   |                                                                                                     |

### 4.2. Queues

Default arguments for critical queues: `{"x-dead-letter-exchange": "ex.dead_letter", "x-ha-policy": "all"}` (HA policy applied separately).

| Name                                      | VHost                | Durability | Auto-delete | Arguments (Example: DLX, TTL, HA Policy)                                | Purpose                                                                             | Bound to Exchange (Routing Key)                         |
| :---------------------------------------- | :------------------- | :--------- | :---------- | :---------------------------------------------------------------------- | :---------------------------------------------------------------------------------- | :------------------------------------------------------ |
| `q.ai_generation.pending`                 | `/creativeflow_prod` | true       | false       | `{"x-dead-letter-exchange": "ex.dead_letter", "x-message-ttl": 3600000}` | New AI generation jobs for n8n. (Matches `AiGenerationJobsQueue` from config)      | `ex.creativeflow.direct` (rk: `ai.generation.request`)  |
| `q.ai_generation.samples_ready`           | `/creativeflow_prod` | true       | false       | `{"x-dead-letter-exchange": "ex.dead_letter"}`                          | n8n signals samples are ready.                                                      | `ex.creativeflow.topic` (rk: `ai.event.samples.ready.#`)  |
| `q.ai_generation.final_request`           | `/creativeflow_prod` | true       | false       | `{"x-dead-letter-exchange": "ex.dead_letter"}`                          | User requests final high-res generation.                                            | `ex.creativeflow.direct` (rk: `ai.generation.final`)    |
| `q.ai_generation.completed`               | `/creativeflow_prod` | true       | false       | `{"x-dead-letter-exchange": "ex.dead_letter"}`                          | Final asset generated, for Odoo/Notification Service.                               | `ex.creativeflow.topic` (rk: `ai.event.completed.#`)    |
| `q.ai_generation.failed`                  | `/creativeflow_prod` | true       | false       | `{"x-dead-letter-exchange": "ex.dead_letter"}`                          | Failed AI generations, for Odoo/Notification/Alerting.                              | `ex.creativeflow.topic` (rk: `ai.event.failed.#`)       |
| `q.odoo.events`                           | `/creativeflow_prod` | true       | false       | `{"x-dead-letter-exchange": "ex.dead_letter"}`                          | Generic Odoo business events for n8n or other services. (Matches `OdooEventsTopicQueue`)| `ex.creativeflow.topic` (rk: `odoo.event.#`)            |
| `q.n8n.task_results`                      | `/creativeflow_prod` | true       | false       | `{"x-dead-letter-exchange": "ex.dead_letter"}`                          | Results from n8n workflows back to Odoo/originator. (Matches `N8nTaskResultsQueue`) | `ex.creativeflow.direct` (rk: `n8n.result.odoo`)        |
| `q.notifications.user_alerts`             | `/creativeflow_prod` | true       | false       | `{"x-dead-letter-exchange": "ex.dead_letter"}`                          | Events for Notification Service to send to users.                                   | `ex.creativeflow.topic` (rk: `notification.user.#`)     |
| `q.collaboration.updates`                 | `/creativeflow_prod` | true       | false       | `{"x-dead-letter-exchange": "ex.dead_letter"}`                          | Real-time collaboration changes for Notification Service.                           | `ex.creativeflow.topic` (rk: `collaboration.update.#`)  |
| `q.dead_letter`                           | `/creativeflow_prod` | true       | false       | `{}`                                                                    | Collects all dead-lettered messages for investigation.                              | `ex.dead_letter` (rk: `#`)                               |
| *(Staging equivalents with `/creativeflow_staging` vhost)* |                      |            |             |                                                                         |                                                                                     |                                                         |

### 4.3. Bindings

Bindings connect exchanges to queues (or exchanges to exchanges).
*   `q.ai_generation.pending` bound to `ex.creativeflow.direct` with routing key `ai.generation.request`.
*   `q.odoo.events` bound to `ex.creativeflow.topic` with routing key `odoo.event.#`.
*   `q.notifications.user_alerts` bound to `ex.creativeflow.topic` with routing key `notification.user.#`.
*   `q.dead_letter` bound to `ex.dead_letter` with routing key `#` (to catch all messages routed to it).
*   Other queues bound appropriately as per their purpose and the exchange type.

## 5. High Availability and Clustering

*   **Clustering:** Nodes will be clustered using classic config peer discovery initially, managed by `join_node.sh`. Erlang cookie (`RABBITMQ_ERLANG_COOKIE`) must be identical across all nodes and securely managed.
*   **Mirrored Queues:** Critical queues (all application queues listed above, except potentially `q.dead_letter` if transient issues are acceptable there) will be mirrored across all nodes in the cluster. This will be achieved using HA policies.
    *   Policy Name: `ha-all-critical-queues`
    *   Pattern: `^q\.(ai|odoo|n8n|notifications|collaboration)\..*` (or more specific patterns if needed)
    *   Definition: `{"ha-mode":"all", "ha-sync-mode":"automatic"}` (Matches `DefaultHaMode` and `DefaultHaSyncMode` from config object)
    *   Apply to: `queues`
    *   Priority: `0`
    *   This policy will be applied using `apply_ha_policies.py`.

## 6. Policies

Beyond HA policies:
*   **Dead Letter Exchanges (DLX):** Queues will be configured with `x-dead-letter-exchange` argument pointing to `ex.dead_letter`. A corresponding `x-dead-letter-routing-key` can be set if specific routing of dead messages is needed.
*   **Message TTL:** Queues like `q.ai_generation.pending` might have a message TTL (`x-message-ttl`) as specified in `QueueDefinitions` to prevent stale jobs from clogging the system. Others may have default TTLs set via policy if required.
    *   Policy Name: `ttl-default-policy` (Example)
    *   Pattern: `.*` (Apply to all queues not having specific TTL)
    *   Definition: `{"message-ttl": 86400000}` (1 day, matches `MessageTTLDefault`)
    *   Apply to: `queues`
    *   Priority: Low (e.g., -1), so specific queue arguments override it.

## 7. Management and Monitoring Scripts

### 7.1. Shell Scripts (`src/scripts/shell/cluster/`)

*   **`join_node.sh`**
    *   **Purpose:** Automate adding a RabbitMQ node to an existing cluster.
    *   **Input:** Master node name (e.g., `rabbit@master_node_hostname`) as a command-line argument.
    *   **Logic:**
        1.  `rabbitmqctl stop_app`
        2.  `rabbitmqctl reset` (Caution: Clears node data)
        3.  `rabbitmqctl join_cluster <master_node_name> [--ram]` (Consider --ram for diskless nodes if applicable, usually not for durable queues)
        4.  `rabbitmqctl start_app`
        5.  Error checking and logging at each step.
*   **`check_cluster_status.sh`**
    *   **Purpose:** Display RabbitMQ cluster status.
    *   **Input:** None.
    *   **Logic:**
        1.  `rabbitmqctl cluster_status`
        2.  Optionally parse output for key indicators (running nodes, partitions) and exit with appropriate status code for automated checks.

### 7.2. Python Scripts (`src/scripts/python/`)

All Python scripts will utilize `src/scripts/python/utils/rabbitmq_api_client.py` for interacting with the RabbitMQ Management HTTP API. They will read API URL and credentials from environment variables: `RABBITMQ_MANAGEMENT_API_URL`, `RABBITMQ_MANAGEMENT_USER`, `RABBITMQ_MANAGEMENT_PASSWORD`. Logging level controlled by `PYTHON_SCRIPT_LOG_LEVEL`.

*   **`utils/rabbitmq_api_client.py`**
    *   **Purpose:** Reusable client for RabbitMQ Management API.
    *   **Class `RabbitMQApiClient`:**
        *   `__init__(self, api_url, username, password)`: Initializes client with API base URL and credentials.
        *   `_request(self, method, path, json_payload=None, params=None)`: Private helper for making HTTP requests using `requests` library with basic auth, error handling, and JSON response parsing.
        *   `get_overview(self)`: GET `/api/overview`.
        *   `list_vhosts(self)`: GET `/api/vhosts`.
        *   `get_vhost(self, vhost_name)`: GET `/api/vhosts/{vhost_name}`.
        *   `create_vhost(self, vhost_name)`: PUT `/api/vhosts/{vhost_name}`.
        *   `delete_vhost(self, vhost_name)`: DELETE `/api/vhosts/{vhost_name}`.
        *   `list_users(self)`: GET `/api/users`.
        *   `get_user(self, username)`: GET `/api/users/{username}`.
        *   `create_user(self, username, password_hash, tags="")`: PUT `/api/users/{username}` with payload `{"password_hash": "...", "tags": "..."}`.
        *   `delete_user(self, username)`: DELETE `/api/users/{username}`.
        *   `list_permissions_for_user(self, username)`: GET `/api/users/{username}/permissions`.
        *   `list_permissions_in_vhost(self, vhost)`: GET `/api/permissions/{vhost}`.
        *   `set_permissions(self, username, vhost, configure_regex, write_regex, read_regex)`: PUT `/api/permissions/{vhost}/{username}` with payload.
        *   `list_exchanges(self, vhost)`: GET `/api/exchanges/{vhost}`.
        *   `create_exchange(self, vhost, exchange_name, type, durable, auto_delete, internal=False, arguments=None)`: PUT `/api/exchanges/{vhost}/{exchange_name}`.
        *   `list_queues(self, vhost)`: GET `/api/queues/{vhost}`.
        *   `create_queue(self, vhost, queue_name, durable, auto_delete, arguments=None)`: PUT `/api/queues/{vhost}/{queue_name}`.
        *   `create_binding(self, vhost, source_exchange, destination_type, destination_name, routing_key, arguments=None)`: POST `/api/bindings/{vhost}/e/{source_exchange}/{destination_type}/{destination_name}`.
        *   `list_policies(self, vhost)`: GET `/api/policies/{vhost}`.
        *   `set_policy(self, vhost, policy_name, pattern, definition, priority=0, apply_to="all")`: PUT `/api/policies/{vhost}/{policy_name}`.
        *   `get_nodes(self)`: GET `/api/nodes`.
        *   `get_queue_metrics(self, vhost, queue_name)`: GET `/api/queues/{vhost}/{queue_name}`.

*   **`security/manage_users.py`**
    *   **Purpose:** Manage users and permissions.
    *   **Command-line interface (using `argparse`):**
        *   `add_user --username <name> --password <pass> [--tags <tags>]` (password will be hashed by RabbitMQ if sent plaintext, or pre-hashed if supported by API client)
        *   `delete_user --username <name>`
        *   `list_users`
        *   `set_permissions --username <name> --vhost <vhost> --configure <regex> --write <regex> --read <regex>`
    *   **Logic:** Uses `RabbitMQApiClient` to perform actions.

*   **`topology/declare_entities.py`**
    *   **Purpose:** Declare vhosts, exchanges, queues, bindings from a config file.
    *   **Input:** Path to a YAML/JSON configuration file.
    *   **Config File Structure (YAML example):**
        yaml
        vhosts:
          - name: /creativeflow_prod
          - name: /creativeflow_staging
        exchanges:
          - vhost: /creativeflow_prod
            name: ex.creativeflow.direct
            type: direct
            durable: true
            # ... other exchanges
        queues:
          - vhost: /creativeflow_prod
            name: q.ai_generation.pending
            durable: true
            arguments:
              x-dead-letter-exchange: ex.dead_letter
              x-message-ttl: 3600000 # From QueueDefinitions
            # ... other queues
        bindings:
          - vhost: /creativeflow_prod
            source_exchange: ex.creativeflow.direct
            destination_type: queue # 'queue' or 'exchange'
            destination_name: q.ai_generation.pending
            routing_key: ai.generation.request
            # ... other bindings
        
    *   **Logic:**
        1.  Parses the config file using `PyYAML` or `json`.
        2.  Uses `RabbitMQApiClient` to idempotently declare entities. Checks if entity exists before creating to avoid errors on re-runs.
        3.  Handles creation order (vhosts, then exchanges/queues, then bindings).

*   **`policies/apply_ha_policies.py`**
    *   **Purpose:** Apply HA and other policies.
    *   **Input:** Path to a YAML/JSON policy configuration file or individual policy parameters via CLI.
    *   **Policy Config File Structure (YAML example):**
        yaml
        policies:
          - vhost: /creativeflow_prod
            name: ha-all-critical-queues
            pattern: "^q\\.(ai|odoo|n8n|notifications|collaboration)\\..*"
            definition:
              ha-mode: all # From DefaultHaMode
              ha-sync-mode: automatic # From DefaultHaSyncMode
            priority: 0
            apply-to: queues
          - vhost: /creativeflow_prod
            name: default-message-ttl
            pattern: ".*" # Generic, overridden by specific queue TTLs
            definition:
              message-ttl: 86400000 # From MessageTTLDefault
            priority: -1 # Low priority
            apply-to: queues
        
    *   **Logic:** Uses `RabbitMQApiClient` to set policies.

*   **`monitoring/export_metrics.py`**
    *   **Purpose:** Export RabbitMQ metrics for Prometheus.
    *   **Output Format:** Prometheus text format.
    *   **Key Metrics to Export (examples):**
        *   `rabbitmq_overview_messages_ready`
        *   `rabbitmq_overview_messages_unacked`
        *   `rabbitmq_queue_messages_ready{vhost="...", queue="..."}`
        *   `rabbitmq_queue_messages_unacked{vhost="...", queue="..."}`
        *   `rabbitmq_queue_consumers{vhost="...", queue="..."}`
        *   `rabbitmq_node_disk_free_bytes{node="..."}`
        *   `rabbitmq_node_mem_used_bytes{node="..."}`
        *   `rabbitmq_node_fd_used{node="..."}`
        *   `rabbitmq_node_sockets_used{node="..."}`
        *   `rabbitmq_node_running{node="..."}` (1 if running, 0 if not)
        *   `rabbitmq_connections_total`
        *   `rabbitmq_channels_total`
    *   **Logic:**
        1.  Uses `RabbitMQApiClient` to fetch data from `/api/overview`, `/api/nodes`, `/api/queues/{vhost}/{queue}`.
        2.  Formats metrics into Prometheus text lines.
        3.  Either writes to a file for `node_exporter`'s textfile collector or runs as an HTTP server exposing a `/metrics` endpoint.

## 8. Security Considerations

*   **Erlang Cookie:** `RABBITMQ_ERLANG_COOKIE` must be a long, random, shared secret across all cluster nodes. Managed by Ansible and Vault.
*   **Management Plugin:**
    *   Access restricted by firewall rules.
    *   Strong credentials for management users (`rabbitmq_admin_app`, `monitoring_agent`).
    *   Consider enabling SSL/TLS for the Management Plugin HTTP API.
*   **AMQP:**
    *   Consider enabling SSL/TLS for AMQP client connections.
    *   Application users (`odoo_svc`, `n8n_worker`, etc.) should have least-privilege permissions.
*   **Passwords:** All passwords (initial default, script users) must be strong. Application service passwords for RabbitMQ should be managed via a secrets manager (e.g., HashiCorp Vault) and injected into application configurations, not hardcoded.
*   **Network Segmentation:** RabbitMQ nodes should reside in a secured network segment, with firewall rules controlling access to AMQP and management ports.

## 9. Operational Procedures (Outline)

*   **Initial Cluster Setup:** Use Ansible to deploy RabbitMQ, configure `rabbitmq.conf`, `advanced.config`, set Erlang cookie, start first node. Then use `join_node.sh` (or Ansible playbook wrapping it) to add subsequent nodes. Import `production_definitions.json` or run `declare_entities.py` and `apply_ha_policies.py`. Create users via `manage_users.py`.
*   **Adding/Removing Nodes:** Use `join_node.sh` for adding. For removal, `rabbitmqctl forget_cluster_node <nodename>`.
*   **Status Checks:** Use `check_cluster_status.sh` and Prometheus/Grafana monitoring.
*   **Backup:** Regularly export definitions using RabbitMQ Management Plugin or `rabbitmqadmin` tool (not covered by these scripts but an operational task). Ansible should back up configuration files (`*.conf`, `*.config`).
*   **Restore (Definitions):** Import saved `_definitions.json` via Management Plugin or UI.
*   **Monitoring:** Prometheus scraping metrics from `export_metrics.py` or RabbitMQ's native Prometheus endpoint. Alerts set up in Alertmanager/Grafana for queue depths, consumer counts, node health, message rates, disk/memory watermarks.
*   **Patching/Upgrades:** Follow RabbitMQ documentation for rolling upgrades if possible, coordinated with Ansible updates.

## 10. Environment Variables Summary

*   `RABBITMQ_NODENAME`: e.g., `rabbit@${HOSTNAME}` (often set in `rabbitmq-env.conf` or systemd unit)
*   `RABBITMQ_ERLANG_COOKIE`: Secure shared secret for clustering.
*   `RABBITMQ_MANAGEMENT_API_URL`: e.g., `http://localhost:15672` (for Python scripts, if not run on a RabbitMQ node directly)
*   `RABBITMQ_MANAGEMENT_USER`: User for Python scripts accessing management API (e.g., `rabbitmq_admin_app`).
*   `RABBITMQ_MANAGEMENT_PASSWORD`: Password for the management API user.
*   `PYTHON_SCRIPT_LOG_LEVEL`: e.g., `INFO`, `DEBUG`.
*   `ANSIBLE_VAULT_PASSWORD_FILE`: For Ansible to decrypt secrets.

## 11. Configuration Input for `declare_entities.py`

The `declare_entities.py` script will expect a YAML or JSON configuration file defining the topology. Below is an example structure for YAML:

yaml
# rabbitmq_topology.yaml
vhosts:
  - name: /creativeflow_prod
    description: "Production virtual host for CreativeFlow AI"
  - name: /creativeflow_staging
    description: "Staging virtual host for CreativeFlow AI"

exchanges:
  - vhost: /creativeflow_prod # or /creativeflow_staging
    name: ex.creativeflow.direct
    type: direct
    durable: true
    auto_delete: false
    internal: false
    arguments: {}
  - vhost: /creativeflow_prod
    name: ex.creativeflow.topic
    type: topic
    durable: true
    auto_delete: false
    internal: false
    arguments: {}
  - vhost: /creativeflow_prod
    name: ex.dead_letter # Central DLX
    type: direct # Usually direct for DLX routing
    durable: true
    auto_delete: false
    arguments: {}
  # ... other exchanges for staging

queues:
  - vhost: /creativeflow_prod
    name: q.ai_generation.pending
    durable: true
    auto_delete: false
    arguments:
      x-dead-letter-exchange: "ex.dead_letter"
      x-dead-letter-routing-key: "dlq.ai_generation.pending" # Optional specific routing key for DLQ
      x-message-ttl: 3600000 # 1 hour (from QueueDefinitions)
      # x-ha-policy: "ha-all-critical-queues" # HA policy is applied via RabbitMQ policies, not queue args directly
  - vhost: /creativeflow_prod
    name: q.odoo.events
    durable: true
    auto_delete: false
    arguments:
      x-dead-letter-exchange: "ex.dead_letter"
  - vhost: /creativeflow_prod
    name: q.n8n.task_results
    durable: true
    auto_delete: false
    arguments:
      x-dead-letter-exchange: "ex.dead_letter"
  - vhost: /creativeflow_prod
    name: q.dead_letter # Queue to consume dead-lettered messages
    durable: true
    auto_delete: false
    arguments: {} # No DLX for the DLQ itself usually
  # ... other queues including samples_ready, final_request, completed, failed, notifications, collaboration etc.
  # ... staging equivalents

bindings:
  - vhost: /creativeflow_prod
    source_exchange: ex.creativeflow.direct
    destination_type: queue # 'queue' or 'exchange'
    destination_name: q.ai_generation.pending
    routing_key: ai.generation.request
    arguments: {}
  - vhost: /creativeflow_prod
    source_exchange: ex.creativeflow.topic
    destination_type: queue
    destination_name: q.odoo.events
    routing_key: "odoo.event.#"
    arguments: {}
  - vhost: /creativeflow_prod
    source_exchange: ex.dead_letter # Binding for the DLQ to consume from DLX
    destination_type: queue
    destination_name: q.dead_letter
    routing_key: "#" # Catches all messages routed to ex.dead_letter
  # ... other bindings
  # ... staging equivalents


This structure allows the `declare_entities.py` script to iterate and create the necessary RabbitMQ topology in an idempotent manner.