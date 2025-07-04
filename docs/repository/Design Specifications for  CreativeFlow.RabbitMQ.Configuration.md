# Software Design Specification: CreativeFlow.RabbitMQ.Configuration

## 1. Introduction

### 1.1 Purpose of the Repository
This repository, `CreativeFlow.RabbitMQ.Configuration`, is responsible for defining, applying, and managing the configuration of the RabbitMQ message broker cluster used within the CreativeFlow AI platform. It ensures a consistent, version-controlled, and automatable setup for RabbitMQ entities such as virtual hosts, exchanges, queues, bindings, users, permissions, and operational policies (e.g., High Availability, Dead Letter Exchanges).

### 1.2 Scope
The scope of this repository includes:
*   Declarative definition of the RabbitMQ topology using a JSON configuration file.
*   Shell and Python scripts for applying these definitions to a RabbitMQ cluster.
*   Scripts for managing specific policies (High Availability, Dead Letter Exchanges).
*   Scripts for managing application-specific users and their permissions.
*   Utility scripts for cluster monitoring and operational checks.
*   Templates for environment-specific configurations and credentials.

This repository does *not* include the RabbitMQ server installation itself (which is an infrastructure concern handled by Ansible, as per `CPIO-007` and related DevOps requirements) but provides the means to configure a running instance or cluster.

### 1.3 Target Audience
This document is intended for:
*   **DevOps Engineers**: Responsible for deploying, managing, and automating RabbitMQ configurations.
*   **Backend Developers**: Who need to understand the messaging topology to integrate their services.
*   **System Architects**: For understanding the messaging infrastructure design.

## 2. System Overview

### 2.1 Role of RabbitMQ in CreativeFlow AI
RabbitMQ serves as the central asynchronous messaging backbone for the CreativeFlow AI platform. It decouples various microservices and components, enabling reliable and scalable processing of tasks such as:
*   AI creative generation job requests and results (SRS Section 5.3.1, NFR-005).
*   Inter-service communication (e.g., Odoo backend to n8n, n8n to AI services).
*   Notification dispatching to users.
*   Real-time collaboration event propagation.

This repository ensures that the RabbitMQ cluster is correctly configured to support these functionalities effectively and reliably.

### 2.2 Key Features Managed by this Repository
*   **Topology Definition**: Centralized definition of all RabbitMQ entities.
*   **Automated Configuration**: Scripts to apply the defined topology.
*   **Policy Management**: Scripts for setting HA and DLX policies.
*   **User & Permission Management**: Scripts for managing application service users.
*   **Operational Utilities**: Scripts for cluster status checks and queue monitoring.

## 3. Design Principles

### 3.1 Declarative Configuration
The primary RabbitMQ topology is defined declaratively in a `definitions.json` file. This file acts as the source of truth and allows for version control and easy import/export via the RabbitMQ Management Plugin.

### 3.2 Idempotency of Scripts
All configuration application scripts (`apply_definitions.sh`, `set_ha_policy.sh`, `set_dlx_policy.sh`) are designed to be idempotent. Running them multiple times will result in the same final state without causing errors or unintended side effects.

### 3.3 Security and Secrets Management
*   Sensitive information like passwords for RabbitMQ users defined in `definitions.json` will be pre-hashed.
*   Scripts requiring credentials for the RabbitMQ Management API will use environment variables or configuration files (from templates) that are *not* committed to version control with plaintext secrets. These should be sourced from a secure secret management system (e.g., HashiCorp Vault, Ansible Vault) in CI/CD or deployment environments.
*   Application users created via scripts will have the minimum necessary permissions (Principle of Least Privilege).

### 3.4 Modularity of Scripts
Scripts are organized by function (e.g., applying definitions, setting policies, user management, cluster management) to promote clarity and maintainability.

## 4. Detailed Design of Components

### 4.1 `src/definitions.json`
*   **File Path**: `src/definitions.json`
*   **Description**: Master RabbitMQ definitions file in JSON format. This file declaratively defines vhosts, exchanges, queues, bindings, users (with initial passwords/tags), and permissions.
*   **Purpose**: To provide a comprehensive, declarative configuration for RabbitMQ entities, facilitating easy import and version control of the broker's topology. (Requirement: Section 2.1, 5.1, 5.2.2, 5.3.1, NFR-005)
*   **Implemented Features**: Core RabbitMQ Topology Definition, User Definitions, Permission Definitions, Initial Policy Definitions.
*   **Structure and Logic**: This file adheres to the RabbitMQ management plugin's export/import format.
    *   **`rabbit_version`**: Specifies the RabbitMQ version the definitions are compatible with.
    *   **`users`**: Array of user objects.
        *   Example User (`admin_user`):
            json
            {
              "name": "cf_admin",
              "password_hash": "...", // Strong pre-computed hash
              "hashing_algorithm": "rabbit_password_hashing_sha256", // or sha512
              "tags": "administrator,management,policymaker"
            }
            
        *   Example Application User (`odoo_service`):
            json
            {
              "name": "odoo_service",
              "password_hash": "...",
              "hashing_algorithm": "rabbit_password_hashing_sha256",
              "tags": ""
            }
            
        *   Other users: `n8n_service`, `notification_service`, `collaboration_service`, `monitoring_user`.
    *   **`vhosts`**: Array of virtual host objects.
        *   Primary vhost:
            json
            { "name": "creativeflow_vhost" }
            
    *   **`permissions`**: Array of permission objects.
        *   Example for `cf_admin` on `creativeflow_vhost`:
            json
            {
              "user": "cf_admin",
              "vhost": "creativeflow_vhost",
              "configure": ".*",
              "write": ".*",
              "read": ".*"
            }
            
        *   Example for `odoo_service` (least privilege):
            json
            {
              "user": "odoo_service",
              "vhost": "creativeflow_vhost",
              "configure": "^(q\\.ai\\.generation\\.tasks|q\\.ai\\.generation\\.updates)$", // Configure own queues if needed
              "write": "^(ex\\.direct\\.tasks|ex\\.topic\\.platform_events)$", // Publish to specific exchanges
              "read": "^(q\\.ai\\.generation\\.updates)$" // Consume from specific queues
            }
            
        *   Define permissions for `n8n_service`, `notification_service`, `collaboration_service`, `monitoring_user` similarly.
    *   **`exchanges`**: Array of exchange objects.
        *   `ex.direct.tasks` (type: `direct`, durable: `true`)
        *   `ex.topic.platform_events` (type: `topic`, durable: `true`)
        *   `ex.fanout.notifications` (type: `fanout`, durable: `true`)
        *   `ex.dlx` (type: `direct`, durable: `true`, for dead-lettering)
    *   **`queues`**: Array of queue objects.
        *   `q.ai.generation.tasks` (durable: `true`, arguments: `{"x-queue-type": "quorum"}` or HA policy for classic mirrored)
        *   `q.ai.generation.updates` (durable: `true`, arguments: `{"x-queue-type": "quorum"}` or HA policy)
        *   `q.notifications.email` (durable: `true`, arguments: `{"x-queue-type": "quorum"}` or HA policy)
        *   `q.notifications.websocket` (durable: `true`, arguments: `{"x-queue-type": "quorum"}` or HA policy)
        *   `q.collaboration.events` (durable: `true`, arguments: `{"x-queue-type": "quorum"}` or HA policy)
        *   `q.dlx.common` (durable: `true`)
        *   `q.dlx.ai.generation` (durable: `true`)
        *   Other service-specific queues as needed.
    *   **`bindings`**: Array of binding objects.
        *   `q.ai.generation.tasks` to `ex.direct.tasks` with routing key `ai.job.request`.
        *   `q.ai.generation.updates` to `ex.topic.platform_events` with routing key `ai.job.update.#`.
        *   `q.notifications.email` to `ex.topic.platform_events` with routing key `notification.email.#`.
        *   `q.notifications.websocket` to `ex.topic.platform_events` with routing key `notification.websocket.#`.
        *   `q.collaboration.events` to `ex.topic.platform_events` with routing key `collaboration.event.#`.
        *   `q.dlx.common` to `ex.dlx` with routing key `dlx.common`.
        *   `q.dlx.ai.generation` to `ex.dlx` with routing key `dlx.ai.generation`.
    *   **`policies`**: Array of policy objects (can also be managed by scripts for dynamic aspects).
        *   Example HA policy (if not using quorum queues directly):
            json
            {
              "vhost": "creativeflow_vhost",
              "name": "ha-critical",
              "pattern": "^(q\\.ai\\..*|q\\.notifications\\..*|q\\.collaboration\\..*)$",
              "apply-to": "queues",
              "definition": {
                "ha-mode": "all", // or "exactly" with "ha-params"
                "ha-sync-mode": "automatic"
              },
              "priority": 0
            }
            
        *   Example DLX policy for `q.ai.generation.tasks`:
            json
            {
              "vhost": "creativeflow_vhost",
              "name": "dlx-ai-generation-tasks",
              "pattern": "^q\\.ai\\.generation\\.tasks$",
              "apply-to": "queues",
              "definition": {
                "dead-letter-exchange": "ex.dlx",
                "dead-letter-routing-key": "dlx.ai.generation"
                // "message-ttl": 3600000 // Optional: message TTL before DLX
              },
              "priority": 0
            }
            
*   **Security Notes**: Passwords must be pre-hashed. Ensure the JSON file itself has restricted access.

### 4.2 `src/scripts/apply_definitions.sh`
*   **File Path**: `src/scripts/apply_definitions.sh`
*   **Purpose**: To automate the application of the RabbitMQ topology and policies defined in `definitions.json` to a running RabbitMQ cluster. (Requirement: Section 5.2.2, NFR-005)
*   **Implemented Features**: Automated Configuration Deployment.
*   **Logic**:
    1.  Source environment variables from `config/rabbitmq_env.sh` (if it exists) for `RABBITMQ_MANAGEMENT_URL`, `RABBITMQ_USER`, `RABBITMQ_PASS`, `RABBITMQ_DEFAULT_VHOST`.
    2.  Define `DEFINITIONS_FILE` path (e.g., `../definitions.json`).
    3.  Check if `DEFINITIONS_FILE` exists.
    4.  Use `curl` to upload the definitions file:
        bash
        curl -u "${RABBITMQ_USER}:${RABBITMQ_PASS}" \
             -H "content-type:application/json" \
             -X POST \
             "${RABBITMQ_MANAGEMENT_URL}/api/definitions/${RABBITMQ_DEFAULT_VHOST}" \
             -d @"${DEFINITIONS_FILE}"
        
        Alternatively, `rabbitmqadmin` can be used if installed:
        bash
        rabbitmqadmin -H $(echo $RABBITMQ_MANAGEMENT_URL | sed 's|http://||; s|https://||') \
                      -u "${RABBITMQ_USER}" -p "${RABBITMQ_PASS}" \
                      import "${DEFINITIONS_FILE}"
        
    5.  Check the HTTP response code from `curl` (or exit code from `rabbitmqadmin`) for success (e.g., 201 Created or 204 No Content).
    6.  Echo success or error messages.
*   **Configuration**: `RABBITMQ_MANAGEMENT_URL`, `RABBITMQ_USER`, `RABBITMQ_PASS`, `RABBITMQ_DEFAULT_VHOST` (typically `/` or `creativeflow_vhost`).
*   **Error Handling**: Script will exit with a non-zero status on `curl` or `rabbitmqadmin` failure. Output from the command will indicate specific errors.
*   **Security Notes**: Relies on securely provided credentials via environment variables. Avoid hardcoding credentials.

### 4.3 `src/scripts/policies/set_ha_policy.sh`
*   **File Path**: `src/scripts/policies/set_ha_policy.sh`
*   **Purpose**: To apply High Availability (HA) policies to RabbitMQ queues, ensuring messages are replicated across cluster nodes for fault tolerance. (Requirement: DEP-001, NFR-005)
*   **Implemented Features**: High Availability Configuration.
*   **Logic**:
    1.  Source environment variables from `config/rabbitmq_env.sh` for `RABBITMQ_CTL_NODE` (if running `rabbitmqctl` remotely), `RABBITMQ_USER`, `RABBITMQ_PASS` (if needed by `rabbitmqctl` on some setups or for HTTP API approach).
    2.  Accept parameters: `VHOST`, `POLICY_NAME`, `QUEUE_PATTERN`, `HA_DEFINITION_JSON` (e.g., `'{"ha-mode":"all", "ha-sync-mode":"automatic"}'` or `'{"ha-mode":"exactly", "ha-params":2, "ha-sync-mode":"automatic"}'`).
    3.  Construct and execute the `rabbitmqctl set_policy` command:
        bash
        rabbitmqctl set_policy -p "${VHOST}" --apply-to queues "${POLICY_NAME}" "${QUEUE_PATTERN}" "${HA_DEFINITION_JSON}"
        
    4.  Check exit code of `rabbitmqctl` for success.
    5.  Echo success or error.
*   **Configuration**: Script parameters. RabbitMQ control node and credentials might be needed.
*   **Error Handling**: Script will exit with a non-zero status on `rabbitmqctl` failure.
*   **Security Notes**: Ensure `rabbitmqctl` is used securely, potentially requiring specific user tags if not run as administrator.

### 4.4 `src/scripts/policies/set_dlx_policy.sh`
*   **File Path**: `src/scripts/policies/set_dlx_policy.sh`
*   **Purpose**: To configure Dead Letter Exchange (DLX) policies for specified RabbitMQ queues, routing undeliverable messages to a DLX. (Requirement: NFR-005)
*   **Implemented Features**: Dead Letter Exchange Configuration.
*   **Logic**:
    1.  Source environment variables similar to `set_ha_policy.sh`.
    2.  Accept parameters: `VHOST`, `POLICY_NAME`, `QUEUE_PATTERN`, `DLX_NAME`, `DLRK_NAME` (optional dead-letter routing key).
    3.  Construct the policy definition JSON. If `DLRK_NAME` is provided:
        `DLX_DEFINITION_JSON='{"dead-letter-exchange":"'${DLX_NAME}'", "dead-letter-routing-key":"'${DLRK_NAME}'"}'`
        Else:
        `DLX_DEFINITION_JSON='{"dead-letter-exchange":"'${DLX_NAME}'"}'`
    4.  Construct and execute the `rabbitmqctl set_policy` command:
        bash
        rabbitmqctl set_policy -p "${VHOST}" --apply-to queues "${POLICY_NAME}" "${QUEUE_PATTERN}" "${DLX_DEFINITION_JSON}"
        
    5.  Check exit code and report.
*   **Configuration**: Script parameters.
*   **Error Handling**: Script will exit with a non-zero status on `rabbitmqctl` failure.
*   **Security Notes**: As with `set_ha_policy.sh`.

### 4.5 `src/scripts/users_permissions/manage_app_users.py`
*   **File Path**: `src/scripts/users_permissions/manage_app_users.py`
*   **Purpose**: To programmatically manage RabbitMQ users and their permissions using the HTTP API, allowing for more dynamic or complex configurations. (Requirement: Section 5.2.2)
*   **Implemented Features**: Application User Management, Granular Permission Assignment.
*   **Logic**:
    *   Import `requests` and `json`.
    *   Import configuration from `config.rabbitmq_api_client_config` (e.g., `RABBITMQ_API_CONFIG`).
    *   Base URL: `RABBITMQ_API_CONFIG['url']`. Auth: `(RABBITMQ_API_CONFIG['username'], RABBITMQ_API_CONFIG['password'])`.
    *   **`create_user(username, password, tags_list=None)`**:
        *   Endpoint: `PUT /api/users/{username}`.
        *   Body: `{"password": password, "tags": ",".join(tags_list) if tags_list else ""}`.
        *   RabbitMQ will hash the provided plain password.
        *   Handle HTTP response codes (201 Created, 204 No Content for update, 4xx/5xx for errors).
    *   **`set_permissions(username, vhost, configure_regex, write_regex, read_regex)`**:
        *   Endpoint: `PUT /api/permissions/{vhost}/{username}`.
        *   Body: `{"configure": configure_regex, "write": write_regex, "read": read_regex}`.
        *   Handle HTTP response codes.
    *   **`delete_user(username)`**:
        *   Endpoint: `DELETE /api/users/{username}`.
        *   Handle HTTP response codes.
    *   **`list_users()`**: GET `/api/users`.
    *   **`get_user_permissions(username, vhost)`**: GET `/api/permissions/{vhost}/{username}`.
    *   Command-line argument parsing (e.g., using `argparse`) to call these functions with appropriate parameters.
*   **Configuration**: RabbitMQ Management API URL, admin username, and password from `config.rabbitmq_api_client_config`.
*   **Error Handling**: Raise exceptions or print error messages based on HTTP status codes and API responses.
*   **Security Notes**: Credentials for the Management API must be handled securely. This script offers more dynamic control than `definitions.json` for user management post-initial setup.

### 4.6 `src/scripts/cluster_management/check_cluster_status.sh`
*   **File Path**: `src/scripts/cluster_management/check_cluster_status.sh`
*   **Purpose**: To provide a quick way to check the overall health and status of the RabbitMQ cluster using `rabbitmqctl` commands. (Requirement: DEP-001)
*   **Implemented Features**: Cluster Health Monitoring.
*   **Logic**:
    1.  Execute `rabbitmqctl cluster_status`.
    2.  Optionally, grep for key status indicators (e.g., `partitions`, `running_nodes`, individual node status).
    3.  Exit with status 0 if healthy, non-zero if issues are detected or command fails.
    4.  The `get_node_health` function is less critical if `cluster_status` is comprehensive.
*   **Configuration**: May need `RABBITMQ_CTL_NODE` if run remotely.
*   **Error Handling**: Relies on `rabbitmqctl` exit codes.
*   **Security Notes**: Ensure `rabbitmqctl` access is appropriately restricted.

### 4.7 `src/scripts/cluster_management/list_queues_with_counts.py`
*   **File Path**: `src/scripts/cluster_management/list_queues_with_counts.py`
*   **Purpose**: To provide detailed information about queues in the RabbitMQ cluster, including message counts and consumer details, via the HTTP API. (Requirement: Section 5.2.2)
*   **Implemented Features**: Queue Monitoring.
*   **Logic**:
    *   Import `requests`, `json`, and `tabulate` (optional).
    *   Import configuration from `config.rabbitmq_api_client_config`.
    *   **`get_queue_details(vhost=None, queue_name_pattern=None)`**:
        *   If `vhost` is provided, endpoint is `/api/queues/{vhost}`. Else, `/api/queues`.
        *   Fetch data using `requests.get` with authentication.
        *   Parse JSON response (list of queue objects).
        *   Filter by `queue_name_pattern` if provided (client-side regex matching on `name`).
        *   Extract `name`, `vhost`, `messages`, `messages_ready`, `messages_unacknowledged`, `consumers`, `memory`, `state`.
        *   Return list of dictionaries or print formatted table.
    *   Command-line argument parsing for `vhost` and `pattern`.
*   **Configuration**: RabbitMQ Management API URL, admin username, password.
*   **Error Handling**: Handle `requests` exceptions and non-200 HTTP status codes.
*   **Security Notes**: Credentials for Management API access.

### 4.8 `src/requirements.txt`
*   **File Path**: `src/requirements.txt`
*   **Purpose**: To list Python package dependencies required by utility and management scripts within this repository.
*   **Implemented Features**: Dependency Management for Python Scripts.
*   **Content**:
    
    requests>=2.25.0,<3.0.0
    # Optional for list_queues_with_counts.py pretty printing
    # tabulate>=0.8.0,<0.9.0
    

### 4.9 `src/config/rabbitmq_env.sh.template`
*   **File Path**: `src/config/rabbitmq_env.sh.template`
*   **Purpose**: To provide a template for setting up environment variables required by shell scripts to interact with RabbitMQ, promoting secure handling of credentials.
*   **Implemented Features**: Secure Configuration Management.
*   **Content**:
    bash
    #!/bin/bash
    # Copy this file to rabbitmq_env.sh and fill in your actual values.
    # Ensure rabbitmq_env.sh is in .gitignore if it contains secrets.

    # For rabbitmqctl running locally or if user/pass is not embedded in erlang cookie or config
    # export RABBITMQ_USER="cf_admin"
    # export RABBITMQ_PASS="YOUR_ADMIN_PASSWORD"

    # For rabbitmqctl targeting a specific node in a cluster (if not default)
    # export RABBITMQ_CTL_NODE="rabbit@hostname1"

    # For scripts using the Management HTTP API (like apply_definitions.sh via curl)
    export RABBITMQ_MANAGEMENT_URL="http://localhost:15672" # Or your cluster's LB/service discovery address
    export RABBITMQ_ADMIN_USER="cf_admin"
    export RABBITMQ_ADMIN_PASS="YOUR_ADMIN_PASSWORD"
    export RABBITMQ_DEFAULT_VHOST="creativeflow_vhost"

    # Erlang cookie if rabbitmqctl needs to connect to remote nodes and not using default
    # export RABBITMQ_CTL_ERLANG_COOKIE="YOUR_ERLANG_COOKIE_SECRET"
    

### 4.10 `src/config/rabbitmq_api_client_config.py.template`
*   **File Path**: `src/config/rabbitmq_api_client_config.py.template`
*   **Purpose**: To provide a template for Python script configurations, storing RabbitMQ Management API connection details and credentials securely.
*   **Implemented Features**: Secure Configuration Management.
*   **Content**:
    python
    # Copy this file to rabbitmq_api_client_config.py and fill in your details.
    # Ensure rabbitmq_api_client_config.py is added to .gitignore if it contains secrets.

    RABBITMQ_API_CONFIG = {
        'url': 'http://localhost:15672',  # e.g., 'http://rabbitmq-node1:15672' or LB
        'username': 'cf_admin',
        'password': 'YOUR_ADMIN_PASSWORD',
        'default_vhost': 'creativeflow_vhost'
    }
    

## 5. RabbitMQ Topology Design Summary
(Details are primarily in `definitions.json` as described in section 4.1)

*   **Virtual Host**: `creativeflow_vhost` for all application messaging.
*   **Users & Permissions**:
    *   `cf_admin`: Full administrative access for management and initial setup.
    *   Service-specific users (e.g., `odoo_service`, `n8n_service`, `notification_service`, `collaboration_service`): Restricted permissions to publish/consume on necessary exchanges/queues within `creativeflow_vhost`.
    *   `monitoring_user`: Read-only access to monitoring endpoints/stats.
*   **Exchanges**:
    *   `ex.direct.tasks`: For direct routing of commands/tasks.
    *   `ex.topic.platform_events`: For flexible event-based communication using topic routing.
    *   `ex.fanout.notifications`: For broadcasting general notifications.
    *   `ex.dlx`: Central dead-letter exchange.
*   **Queues**:
    *   Task Queues: `q.ai.generation.tasks`, etc.
    *   Event/Update Queues: `q.ai.generation.updates`, `q.notifications.email`, `q.notifications.websocket`, `q.collaboration.events`.
    *   Dead Letter Queues: `q.dlx.common`, `q.dlx.ai.generation`.
*   **Bindings**: Configured to route messages appropriately from exchanges to queues based on routing keys (e.g., `ai.job.request`, `notification.email.#`, `dlx.ai.generation`).
*   **Policies**:
    *   **High Availability**: Critical queues configured for mirroring across cluster nodes (e.g., using Quorum Queues or classic mirrored queues with `ha-mode: all`).
    *   **Dead Lettering**: Processing queues configured with DLX routing to `ex.dlx` and specific dead-letter queues for unprocessable messages.

## 6. Deployment and Management Strategy

### 6.1 Initial Setup
1.  Ensure a RabbitMQ cluster is provisioned and running (handled by separate infrastructure automation, e.g., Ansible playbooks from `CPIO` requirements).
2.  Copy `src/config/rabbitmq_env.sh.template` to `src/config/rabbitmq_env.sh` and populate with appropriate credentials and URLs for the target RabbitMQ cluster.
3.  Copy `src/config/rabbitmq_api_client_config.py.template` to `src/config/rabbitmq_api_client_config.py` and populate.
4.  Execute `src/scripts/apply_definitions.sh` to apply the entire topology defined in `src/definitions.json`. This script should be run against the administrative interface of one of the cluster nodes or its load balancer.

### 6.2 Ongoing Management
*   **Topology Changes**: Modify `src/definitions.json` and re-run `src/scripts/apply_definitions.sh`.
*   **Policy Adjustments**: Use `src/scripts/policies/set_ha_policy.sh` and `src/scripts/policies/set_dlx_policy.sh` for specific policy updates if not covered by a full re-application of `definitions.json`.
*   **User Management**: For dynamic user creation or permission changes beyond the initial definitions, use `src/scripts/users_permissions/manage_app_users.py`.
*   **Monitoring**:
    *   Use `src/scripts/cluster_management/check_cluster_status.sh` for quick health checks or in automated monitoring scripts.
    *   Use `src/scripts/cluster_management/list_queues_with_counts.py` for ad-hoc queue inspection or integration into monitoring dashboards.
*   **CI/CD Integration**:
    *   `apply_definitions.sh` can be integrated into a CI/CD pipeline to apply configurations to different environments (dev, staging, prod).
    *   Policy scripts can also be version-controlled and applied via CI/CD.
    *   Secrets for CI/CD execution must be sourced from the pipeline's secure secret store.

### 6.3 Version Control
All configuration files (`definitions.json`) and scripts are version-controlled in Git. Changes should follow standard Git workflows (branching, pull requests, reviews).

## 7. Dependencies

### 7.1 Software
*   **RabbitMQ**: Version 3.13.2+ (as specified or latest stable).
*   **Erlang**: Version 26.2.5+ (compatible with the chosen RabbitMQ version).
*   **Bash**: Version 5.0+ for shell scripts.
*   **Python**: Version 3.11.9+ for Python scripts.

### 7.2 Python Libraries (as per `src/requirements.txt`)
*   `requests`: For interacting with the RabbitMQ Management HTTP API.
*   `tabulate` (optional): For formatted table output in monitoring scripts.

## 8. Future Considerations
*   **Dynamic Shovels/Federation**: If cross-cluster communication becomes a requirement, scripts for managing shovels or federation links could be added.
*   **Advanced Policy Management**: More sophisticated policy management scripts could be developed if needed.
*   **Integration with Centralized Configuration Management**: While Ansible is used for server setup, these RabbitMQ-specific scripts might be called by Ansible or further integrated into a broader configuration management strategy.
*   **Schema Registry for Message Payloads**: For ensuring consistency in message formats across services (outside RabbitMQ config scope but related).
