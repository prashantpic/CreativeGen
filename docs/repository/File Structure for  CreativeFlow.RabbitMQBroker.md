# Specification

# 1. Files

- **Path:** src/config/rabbitmq.conf  
**Description:** Main RabbitMQ server configuration file. Defines core settings such as network listeners, default user credentials (for initial setup, to be changed), disk paths, resource limits (e.g., file descriptors, memory watermarks), and basic clustering parameters. This file uses the modern key=value format.  
**Template:** RabbitMQ Configuration File  
**Dependency Level:** 0  
**Name:** rabbitmq  
**Type:** Configuration  
**Relative Path:** config/rabbitmq.conf  
**Repository Id:** REPO-RABBITMQ-BROKER-001  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Core Server Configuration
    - Network Listener Setup
    - Resource Limit Definition
    
**Requirement Ids:**
    
    - DEP-001 (RabbitMQ Server specs)
    
**Purpose:** To define fundamental operational parameters for RabbitMQ server nodes.  
**Logic Description:** Contains key-value pairs for various RabbitMQ settings. Example keys include listeners.tcp.default, default_user, default_pass (for initial setup only), disk_free_limit.relative, log.file.level, cluster_formation.peer_discovery_backend.  
**Documentation:**
    
    - **Summary:** Primary configuration file for RabbitMQ. Governs network, resource usage, logging, and basic clustering aspects.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** src/config/advanced.config  
**Description:** Advanced RabbitMQ server configuration file using Erlang terms. Used for settings not available in rabbitmq.conf, such as specific SSL/TLS options, kernel parameters, or fine-grained tuning of internal behaviors. This file complements rabbitmq.conf.  
**Template:** RabbitMQ Advanced Configuration File  
**Dependency Level:** 0  
**Name:** advanced  
**Type:** Configuration  
**Relative Path:** config/advanced.config  
**Repository Id:** REPO-RABBITMQ-BROKER-001  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Advanced SSL/TLS Configuration
    - Kernel Parameter Tuning
    - Fine-grained Behavior Customization
    
**Requirement Ids:**
    
    - DEP-001 (RabbitMQ Server specs)
    
**Purpose:** To specify advanced or less common configuration parameters for RabbitMQ server nodes using Erlang syntax.  
**Logic Description:** Contains Erlang terms defining configurations for RabbitMQ applications like rabbit, kernel, ssl. Example: [{rabbit, [{tcp_listen_options, [{backlog, 128}, {nodelay, true}]}]}].  
**Documentation:**
    
    - **Summary:** Erlang-based configuration file for advanced RabbitMQ settings, supplementing rabbitmq.conf.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** src/definitions/production_definitions.json  
**Description:** JSON file containing exported definitions for the production RabbitMQ environment. Includes vhosts, users, permissions, queues, exchanges, bindings, and policies. Used for initial setup, disaster recovery, or ensuring environment consistency. This file can be imported via the RabbitMQ Management Plugin.  
**Template:** RabbitMQ Definitions JSON  
**Dependency Level:** 1  
**Name:** production_definitions  
**Type:** Definitions  
**Relative Path:** definitions/production_definitions.json  
**Repository Id:** REPO-RABBITMQ-BROKER-001  
**Pattern Ids:**
    
    - DeclarativeConfiguration
    - InfrastructureAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Production Environment State Definition
    - Disaster Recovery Aid
    - Configuration Backup
    
**Requirement Ids:**
    
    - Section 5.1 (RabbitMQ in Arch)
    - NFR-005 (Asynchronous processing via queues)
    
**Purpose:** To provide a declarative snapshot of the production RabbitMQ configuration for setup and recovery.  
**Logic Description:** Standard JSON format produced by RabbitMQ Management Plugin's export definitions feature. Contains arrays for 'rabbit_version', 'users', 'vhosts', 'permissions', 'policies', 'queues', 'exchanges', 'bindings'. Each element defines properties like name, durability, arguments (e.g., for DLX, HA).  
**Documentation:**
    
    - **Summary:** A JSON export of production RabbitMQ entities (users, vhosts, queues, exchanges, policies, etc.) for declarative setup or recovery.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** src/definitions/staging_definitions.json  
**Description:** JSON file containing exported definitions for the staging RabbitMQ environment. Mirrors production_definitions.json structure but tailored for staging (e.g., different user credentials if needed, potentially different resource limits or queue configurations for testing).  
**Template:** RabbitMQ Definitions JSON  
**Dependency Level:** 1  
**Name:** staging_definitions  
**Type:** Definitions  
**Relative Path:** definitions/staging_definitions.json  
**Repository Id:** REPO-RABBITMQ-BROKER-001  
**Pattern Ids:**
    
    - DeclarativeConfiguration
    - InfrastructureAsCode
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Staging Environment State Definition
    - Test Environment Consistency
    
**Requirement Ids:**
    
    - Section 5.1 (RabbitMQ in Arch)
    
**Purpose:** To provide a declarative snapshot of the staging RabbitMQ configuration.  
**Logic Description:** Standard JSON format produced by RabbitMQ Management Plugin's export definitions feature, specific to the staging environment setup.  
**Documentation:**
    
    - **Summary:** A JSON export of staging RabbitMQ entities, mirroring production structure but with staging-specific values.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** src/scripts/shell/cluster/join_node.sh  
**Description:** Shell script to join a RabbitMQ node to an existing cluster. Takes the target master node as an argument. Stops the app, joins the cluster, and starts the app.  
**Template:** Shell Script  
**Dependency Level:** 1  
**Name:** join_node  
**Type:** ManagementScript  
**Relative Path:** scripts/shell/cluster/join_node.sh  
**Repository Id:** REPO-RABBITMQ-BROKER-001  
**Pattern Ids:**
    
    - InfrastructureAutomation
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - RabbitMQ Node Clustering
    
**Requirement Ids:**
    
    - Section 5.1 (RabbitMQ in Arch)
    
**Purpose:** To automate the process of adding a new node to a RabbitMQ cluster.  
**Logic Description:** Uses 'rabbitmqctl stop_app', 'rabbitmqctl reset', 'rabbitmqctl join_cluster <master_node_name>', 'rabbitmqctl start_app'. Includes error checking and logging. Accepts master node name as parameter.  
**Documentation:**
    
    - **Summary:** A shell script to add the current RabbitMQ node to a specified cluster master node.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** OperationalScript
    
- **Path:** src/scripts/shell/cluster/check_cluster_status.sh  
**Description:** Shell script to check and display the status of the RabbitMQ cluster, including running nodes and partitions.  
**Template:** Shell Script  
**Dependency Level:** 1  
**Name:** check_cluster_status  
**Type:** ManagementScript  
**Relative Path:** scripts/shell/cluster/check_cluster_status.sh  
**Repository Id:** REPO-RABBITMQ-BROKER-001  
**Pattern Ids:**
    
    - InfrastructureAutomation
    - MonitoringScript
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - RabbitMQ Cluster Health Check
    
**Requirement Ids:**
    
    - Section 5.1 (RabbitMQ in Arch)
    
**Purpose:** To provide a quick way to verify RabbitMQ cluster health.  
**Logic Description:** Uses 'rabbitmqctl cluster_status'. Parses output for key health indicators. Can be used for automated health checks.  
**Documentation:**
    
    - **Summary:** A shell script to display the current RabbitMQ cluster status.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** OperationalScript
    
- **Path:** src/scripts/python/security/manage_users.py  
**Description:** Python script to manage RabbitMQ users and permissions using the RabbitMQ Management HTTP API. Supports adding, deleting, listing users, and setting permissions per vhost. Uses environment variables for API credentials and endpoint.  
**Template:** Python Script  
**Dependency Level:** 1  
**Name:** manage_users  
**Type:** ManagementScript  
**Relative Path:** scripts/python/security/manage_users.py  
**Repository Id:** REPO-RABBITMQ-BROKER-001  
**Pattern Ids:**
    
    - InfrastructureAutomation
    - APIDrivenConfiguration
    
**Members:**
    
    
**Methods:**
    
    - **Name:** add_user  
**Parameters:**
    
    - username
    - password_hash
    - tags
    
**Return Type:** bool  
**Attributes:** private  
    - **Name:** delete_user  
**Parameters:**
    
    - username
    
**Return Type:** bool  
**Attributes:** private  
    - **Name:** set_permissions  
**Parameters:**
    
    - username
    - vhost
    - configure_regex
    - write_regex
    - read_regex
    
**Return Type:** bool  
**Attributes:** private  
    - **Name:** main  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - User Creation
    - User Deletion
    - Permission Management
    
**Requirement Ids:**
    
    - Section 5.1 (RabbitMQ in Arch)
    
**Purpose:** To automate RabbitMQ user and permission management via its HTTP API.  
**Logic Description:** Uses Python's 'requests' library to interact with RabbitMQ Management API endpoints (e.g., /api/users/<user>, /api/permissions/<vhost>/<user>). Parses command-line arguments for actions (add, delete, set_perms) and parameters. Handles API responses and errors.  
**Documentation:**
    
    - **Summary:** Python script for programmatic management of RabbitMQ users and their permissions using the Management API.
    
**Namespace:** rabbitmq.management.security  
**Metadata:**
    
    - **Category:** OperationalScript
    
- **Path:** src/scripts/python/topology/declare_entities.py  
**Description:** Python script to declare RabbitMQ entities (vhosts, queues, exchanges, bindings) programmatically using a library like Pika for AMQP communication or the RabbitMQ Management HTTP API for more declarative setup. This script would be used for initial setup or ensuring desired topology exists. Configuration for entities can be read from a YAML/JSON file.  
**Template:** Python Script  
**Dependency Level:** 1  
**Name:** declare_entities  
**Type:** ManagementScript  
**Relative Path:** scripts/python/topology/declare_entities.py  
**Repository Id:** REPO-RABBITMQ-BROKER-001  
**Pattern Ids:**
    
    - InfrastructureAutomation
    - DeclarativeConfiguration
    
**Members:**
    
    
**Methods:**
    
    - **Name:** declare_vhost  
**Parameters:**
    
    - vhost_name
    
**Return Type:** void  
**Attributes:** private  
    - **Name:** declare_exchange  
**Parameters:**
    
    - vhost_name
    - exchange_name
    - exchange_type
    - durable
    - auto_delete
    - arguments
    
**Return Type:** void  
**Attributes:** private  
    - **Name:** declare_queue  
**Parameters:**
    
    - vhost_name
    - queue_name
    - durable
    - auto_delete
    - arguments
    
**Return Type:** void  
**Attributes:** private  
    - **Name:** bind_queue_to_exchange  
**Parameters:**
    
    - vhost_name
    - queue_name
    - exchange_name
    - routing_key
    - arguments
    
**Return Type:** void  
**Attributes:** private  
    - **Name:** load_topology_config  
**Parameters:**
    
    - config_file_path
    
**Return Type:** dict  
**Attributes:** private  
    - **Name:** apply_topology  
**Parameters:**
    
    - topology_config
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** main  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - Virtual Host Creation
    - Exchange Declaration
    - Queue Declaration
    - Binding Creation
    - Dead Letter Exchange (DLX/DLQ) Setup
    
**Requirement Ids:**
    
    - Section 5.2.2 (Job Queue Management component)
    - Section 5.3.1 (RabbitMQ role in pipeline)
    - NFR-005 (Asynchronous processing via queues)
    
**Purpose:** To automate the creation and configuration of RabbitMQ vhosts, exchanges, queues, and bindings based on a defined topology.  
**Logic Description:** Uses Pika library to connect to RabbitMQ. Reads a configuration file (e.g., YAML) defining vhosts, exchanges (type, durability), queues (durability, arguments for DLX, HA policy references), and bindings. Iterates through the configuration to declare each entity idempotently. Handles AMQP connection and channel setup. For example, defines queues like 'ai_generation_jobs', 'odoo_events_topic', 'n8n_task_results', and exchanges like 'direct_commands_exchange', 'topic_events_exchange'. Sets up Dead Letter Exchanges for critical queues.  
**Documentation:**
    
    - **Summary:** Python script to programmatically define RabbitMQ topology (vhosts, exchanges, queues, bindings) usually from a configuration file.
    
**Namespace:** rabbitmq.management.topology  
**Metadata:**
    
    - **Category:** OperationalScript
    
- **Path:** src/scripts/python/policies/apply_ha_policies.py  
**Description:** Python script to apply High Availability (HA) policies to queues, typically for mirroring across cluster nodes. Uses the RabbitMQ Management HTTP API. Takes policy name, pattern (for queues), and definition (e.g., ha-mode, ha-params) as input.  
**Template:** Python Script  
**Dependency Level:** 1  
**Name:** apply_ha_policies  
**Type:** ManagementScript  
**Relative Path:** scripts/python/policies/apply_ha_policies.py  
**Repository Id:** REPO-RABBITMQ-BROKER-001  
**Pattern Ids:**
    
    - InfrastructureAutomation
    - APIDrivenConfiguration
    
**Members:**
    
    
**Methods:**
    
    - **Name:** set_policy  
**Parameters:**
    
    - vhost
    - policy_name
    - pattern
    - definition
    - priority
    - apply_to
    
**Return Type:** bool  
**Attributes:** private  
    - **Name:** main  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - High Availability Policy Configuration
    - Queue Mirroring Setup
    
**Requirement Ids:**
    
    - Section 5.1 (RabbitMQ in Arch)
    - NFR-005 (Asynchronous processing via queues)
    
**Purpose:** To automate the application of HA policies for queue mirroring in a RabbitMQ cluster.  
**Logic Description:** Uses Python's 'requests' library to make PUT requests to the RabbitMQ Management API endpoint /api/policies/<vhost>/<policy_name>. Accepts parameters for vhost, policy name, queue pattern (regex), policy definition (ha-mode: all/exactly/nodes, ha-params), priority, and apply-to (queues/exchanges).  
**Documentation:**
    
    - **Summary:** Python script to define and apply RabbitMQ policies, particularly for High Availability (e.g., queue mirroring).
    
**Namespace:** rabbitmq.management.policies  
**Metadata:**
    
    - **Category:** OperationalScript
    
- **Path:** src/scripts/python/utils/rabbitmq_api_client.py  
**Description:** A utility Python module providing a simple client to interact with the RabbitMQ Management HTTP API. Encapsulates common request patterns (GET, POST, PUT, DELETE) and authentication. Used by other Python management scripts.  
**Template:** Python Module  
**Dependency Level:** 0  
**Name:** rabbitmq_api_client  
**Type:** Utility  
**Relative Path:** scripts/python/utils/rabbitmq_api_client.py  
**Repository Id:** REPO-RABBITMQ-BROKER-001  
**Pattern Ids:**
    
    - APIClient
    - Wrapper
    
**Members:**
    
    - **Name:** api_base_url  
**Type:** str  
**Attributes:** private  
    - **Name:** username  
**Type:** str  
**Attributes:** private  
    - **Name:** password  
**Type:** str  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - api_url
    - username
    - password
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** _request  
**Parameters:**
    
    - method
    - path
    - json_payload=None
    
**Return Type:** requests.Response  
**Attributes:** private  
    - **Name:** get_overview  
**Parameters:**
    
    
**Return Type:** dict  
**Attributes:** public  
    - **Name:** list_queues  
**Parameters:**
    
    - vhost
    
**Return Type:** list  
**Attributes:** public  
    - **Name:** create_user  
**Parameters:**
    
    - username
    - password_hash
    - tags
    
**Return Type:** bool  
**Attributes:** public  
    
**Implemented Features:**
    
    - RabbitMQ Management API Abstraction
    
**Requirement Ids:**
    
    
**Purpose:** To provide a reusable client for interacting with the RabbitMQ Management API from Python scripts.  
**Logic Description:** Uses the 'requests' library for HTTP communication. Handles basic authentication. Provides methods for common API operations like getting cluster overview, listing queues, creating users, setting policies, etc. Reads API URL and credentials from environment variables or configuration.  
**Documentation:**
    
    - **Summary:** A helper module for Python scripts to interact with the RabbitMQ Management HTTP API.
    
**Namespace:** rabbitmq.utils  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** src/scripts/python/monitoring/export_metrics.py  
**Description:** Python script to fetch metrics from RabbitMQ Management API (e.g., queue depths, message rates, consumer counts, node health) and format them for ingestion into a monitoring system like Prometheus (e.g., writing to a file for node_exporter's textfile collector or exposing an HTTP endpoint).  
**Template:** Python Script  
**Dependency Level:** 1  
**Name:** export_metrics  
**Type:** MonitoringScript  
**Relative Path:** scripts/python/monitoring/export_metrics.py  
**Repository Id:** REPO-RABBITMQ-BROKER-001  
**Pattern Ids:**
    
    - MonitoringAgent
    - Exporter
    
**Members:**
    
    
**Methods:**
    
    - **Name:** fetch_rabbitmq_metrics  
**Parameters:**
    
    - api_client
    
**Return Type:** dict  
**Attributes:** private  
    - **Name:** format_metrics_for_prometheus  
**Parameters:**
    
    - metrics_data
    
**Return Type:** str  
**Attributes:** private  
    - **Name:** main  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - RabbitMQ Metrics Collection
    - Prometheus Metrics Formatting
    
**Requirement Ids:**
    
    - DEP-001 (RabbitMQ Server specs implies monitoring)
    
**Purpose:** To extract key RabbitMQ metrics for monitoring purposes.  
**Logic Description:** Uses the 'rabbitmq_api_client.py' utility to query various endpoints of the RabbitMQ Management API (e.g., /api/overview, /api/nodes, /api/queues). Parses the JSON responses to extract relevant metrics. Formats these metrics into Prometheus text format. Can be run periodically via cron or as a simple HTTP server itself if exposing metrics directly.  
**Documentation:**
    
    - **Summary:** Python script to collect metrics from RabbitMQ and expose them for monitoring systems like Prometheus.
    
**Namespace:** rabbitmq.monitoring  
**Metadata:**
    
    - **Category:** MonitoringScript
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - EnableMirroredQueuesGlobally
  - AutoDeclareQueuesOnStartup
  
- **Database Configs:**
  
  
- **Environment Variables:**
  
  - RABBITMQ_NODENAME
  - RABBITMQ_ERLANG_COOKIE
  - RABBITMQ_MANAGEMENT_API_URL
  - RABBITMQ_MANAGEMENT_USER
  - RABBITMQ_MANAGEMENT_PASSWORD
  - PYTHON_SCRIPT_LOG_LEVEL
  
- **Service Endpoints:**
  
  - RABBITMQ_AMQP_PORT
  - RABBITMQ_MANAGEMENT_HTTP_PORT
  
- **Policy Parameters:**
  
  - DefaultHaMode: all
  - DefaultHaSyncMode: automatic
  - DefaultDlqExchangeName: dead_letter_exchange
  - MessageTTLDefault: 86400000
  
- **Queue Definitions:**
  
  - AiGenerationJobsQueue: { durable: true, arguments: {'x-dead-letter-exchange': 'dlx_name', 'x-message-ttl': 3600000} }
  - OdooEventsTopicQueue: { durable: true, arguments: {'x-dead-letter-exchange': 'dlx_name'} }
  - N8nTaskResultsQueue: { durable: true, arguments: {'x-dead-letter-exchange': 'dlx_name'} }
  


---

