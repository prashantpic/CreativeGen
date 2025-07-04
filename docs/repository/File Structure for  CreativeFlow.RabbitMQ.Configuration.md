# Specification

# 1. Files

- **Path:** src/definitions.json  
**Description:** Master RabbitMQ definitions file in JSON format. This file declaratively defines vhosts, exchanges, queues, bindings, users (with initial passwords/tags), and permissions. It can be imported directly using the RabbitMQ Management Plugin. This serves as the primary source of truth for the static topology of the message broker. Policies for HA, DLX etc. can also be part of this file or managed separately via scripts.  
**Template:** RabbitMQ Definitions JSON  
**Dependency Level:** 0  
**Name:** definitions  
**Type:** Configuration  
**Relative Path:** definitions.json  
**Repository Id:** REPO-RABBITMQ-CONFIGURATION-001  
**Pattern Ids:**
    
    - DeclarativeConfiguration
    
**Members:**
    
    - **Name:** rabbit_version  
**Type:** string  
**Attributes:** readonly  
    - **Name:** users  
**Type:** array  
**Attributes:** readonly  
    - **Name:** vhosts  
**Type:** array  
**Attributes:** readonly  
    - **Name:** permissions  
**Type:** array  
**Attributes:** readonly  
    - **Name:** policies  
**Type:** array  
**Attributes:** readonly  
    - **Name:** queues  
**Type:** array  
**Attributes:** readonly  
    - **Name:** exchanges  
**Type:** array  
**Attributes:** readonly  
    - **Name:** bindings  
**Type:** array  
**Attributes:** readonly  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Core RabbitMQ Topology Definition
    - User Definitions
    - Permission Definitions
    - Initial Policy Definitions
    
**Requirement Ids:**
    
    - Section 2.1 (RabbitMQ for async)
    - Section 5.1 (RabbitMQ in Arch)
    - Section 5.2.2 (Job Queue Management component)
    - Section 5.3.1 (RabbitMQ in pipeline)
    - NFR-005 (Asynchronous processing via queues)
    
**Purpose:** To provide a comprehensive, declarative configuration for RabbitMQ entities, facilitating easy import and version control of the broker's topology.  
**Logic Description:** This file is a JSON structure adhering to the RabbitMQ management plugin's export/import format. It will list all necessary exchanges (e.g., 'creativeflow.direct', 'creativeflow.topic.aievents'), queues (e.g., 'q.ai.generation.requests', 'q.notifications.email', 'q.dlx.ai.generation'), bindings between them, virtual hosts, application users with their tags (e.g., 'management', 'policymaker', 'monitoring') and hashed passwords, and permissions for these users on vhosts/exchanges/queues. It will also include basic policies like HA for critical queues and DLX configurations.  
**Documentation:**
    
    - **Summary:** Master JSON file for defining RabbitMQ entities like exchanges, queues, users, and policies. Intended for import via the RabbitMQ Management Plugin.
    
**Namespace:** N/A  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** src/scripts/apply_definitions.sh  
**Description:** Shell script to apply the RabbitMQ configurations defined in 'definitions.json' using rabbitmqctl or the RabbitMQ Management HTTP API (e.g., via curl). This script ensures the broker state matches the declarative configuration. It may include checks for existing entities to avoid errors on re-runs.  
**Template:** Shell Script  
**Dependency Level:** 1  
**Name:** apply_definitions  
**Type:** UtilityScript  
**Relative Path:** scripts/apply_definitions.sh  
**Repository Id:** REPO-RABBITMQ-CONFIGURATION-001  
**Pattern Ids:**
    
    - IdempotentOperation
    
**Members:**
    
    - **Name:** RABBITMQ_USER  
**Type:** string  
**Attributes:** environment  
    - **Name:** RABBITMQ_PASS  
**Type:** string  
**Attributes:** environment  
    - **Name:** RABBITMQ_HOST  
**Type:** string  
**Attributes:** environment  
    - **Name:** DEFINITIONS_FILE  
**Type:** string  
**Attributes:** variable  
    
**Methods:**
    
    - **Name:** import_definitions  
**Parameters:**
    
    - definitions_file_path
    
**Return Type:** void  
**Attributes:** function  
    
**Implemented Features:**
    
    - Automated Configuration Deployment
    
**Requirement Ids:**
    
    - Section 5.2.2 (Job Queue Management component)
    - NFR-005 (Asynchronous processing via queues)
    
**Purpose:** To automate the application of the RabbitMQ topology and policies defined in definitions.json to a running RabbitMQ cluster.  
**Logic Description:** This script will use 'rabbitmqadmin' (Python tool for management API) or 'curl' with 'jq' to interact with the RabbitMQ Management HTTP API. It will take 'definitions.json' as input. The primary action will be to call the API endpoint for importing definitions (e.g., POST /api/definitions). Error handling will be implemented to report success or failure. The script should be idempotent, meaning running it multiple times has the same effect as running it once. It might first try to delete existing entities if a clean slate is required, or rely on RabbitMQ's import behavior for updates.  
**Documentation:**
    
    - **Summary:** Shell script for applying RabbitMQ configurations from a definitions.json file to a RabbitMQ cluster using the management API or rabbitmqctl.
    
**Namespace:** N/A  
**Metadata:**
    
    - **Category:** DeploymentScript
    
- **Path:** src/scripts/policies/set_ha_policy.sh  
**Description:** Shell script using rabbitmqctl to define or update High Availability (HA) policies for specified queues or exchanges (e.g., mirrored queues for critical task processing). This ensures message durability and availability across a RabbitMQ cluster. It will target queues like 'q.ai.generation.requests'.  
**Template:** Shell Script  
**Dependency Level:** 1  
**Name:** set_ha_policy  
**Type:** UtilityScript  
**Relative Path:** scripts/policies/set_ha_policy.sh  
**Repository Id:** REPO-RABBITMQ-CONFIGURATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** VHOST  
**Type:** string  
**Attributes:** variable  
    - **Name:** POLICY_NAME  
**Type:** string  
**Attributes:** variable  
    - **Name:** QUEUE_PATTERN  
**Type:** string  
**Attributes:** variable  
    - **Name:** HA_MODE  
**Type:** string  
**Attributes:** variable  
    - **Name:** HA_PARAMS  
**Type:** string  
**Attributes:** variable  
    
**Methods:**
    
    - **Name:** apply_ha_policy  
**Parameters:**
    
    - vhost
    - policy_name
    - pattern
    - ha_mode
    - ha_params
    
**Return Type:** void  
**Attributes:** function  
    
**Implemented Features:**
    
    - High Availability Configuration
    
**Requirement Ids:**
    
    - DEP-001 (RabbitMQ Server specs - implies clustering)
    - NFR-005 (Asynchronous processing via queues - implies reliability)
    
**Purpose:** To apply High Availability (HA) policies to RabbitMQ queues, ensuring messages are replicated across cluster nodes for fault tolerance.  
**Logic Description:** This script will use 'rabbitmqctl set_policy'. It will define a policy, for example, named 'ha-critical-queues', applying to queues matching a pattern like 'q.ai.*' or 'q.critical.*'. The policy definition will specify 'ha-mode: all' or 'ha-mode: exactly' with 'ha-params' for the number of mirrors. It will apply this policy to the relevant virtual host. The script should be idempotent. Parameters for vhost, policy name, queue pattern, and HA settings will be configurable.  
**Documentation:**
    
    - **Summary:** Applies High Availability policies to specified RabbitMQ queues using rabbitmqctl. This helps in ensuring message durability in a clustered setup.
    
**Namespace:** N/A  
**Metadata:**
    
    - **Category:** ConfigurationScript
    
- **Path:** src/scripts/policies/set_dlx_policy.sh  
**Description:** Shell script using rabbitmqctl to define or update Dead Letter Exchange (DLX) policies for queues. This ensures that messages that cannot be processed are routed to a specified DLX for later inspection or reprocessing. It will target queues like 'q.ai.generation.requests' to route to 'q.dlx.ai.generation'.  
**Template:** Shell Script  
**Dependency Level:** 1  
**Name:** set_dlx_policy  
**Type:** UtilityScript  
**Relative Path:** scripts/policies/set_dlx_policy.sh  
**Repository Id:** REPO-RABBITMQ-CONFIGURATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** VHOST  
**Type:** string  
**Attributes:** variable  
    - **Name:** POLICY_NAME  
**Type:** string  
**Attributes:** variable  
    - **Name:** QUEUE_PATTERN  
**Type:** string  
**Attributes:** variable  
    - **Name:** DLX_NAME  
**Type:** string  
**Attributes:** variable  
    - **Name:** DLRK_NAME  
**Type:** string  
**Attributes:** variable  
    
**Methods:**
    
    - **Name:** apply_dlx_policy  
**Parameters:**
    
    - vhost
    - policy_name
    - pattern
    - dlx_name
    - dlrk_name
    
**Return Type:** void  
**Attributes:** function  
    
**Implemented Features:**
    
    - Dead Letter Exchange Configuration
    
**Requirement Ids:**
    
    - NFR-005 (Asynchronous processing via queues - implies robust error handling)
    
**Purpose:** To configure Dead Letter Exchange (DLX) policies for specified RabbitMQ queues, routing undeliverable messages to a DLX.  
**Logic Description:** This script will use 'rabbitmqctl set_policy'. It will define a policy, for example, named 'dlx-for-ai-queues', applying to queues like 'q.ai.generation.requests'. The policy definition will include 'dead-letter-exchange: creativeflow.dlx' and potentially 'dead-letter-routing-key'. It will ensure the target DLX and corresponding dead-letter queue are defined (likely in definitions.json). Parameters for vhost, policy name, queue pattern, and DLX name will be configurable.  
**Documentation:**
    
    - **Summary:** Configures Dead Letter Exchange policies for RabbitMQ queues using rabbitmqctl. This is crucial for handling messages that cannot be processed.
    
**Namespace:** N/A  
**Metadata:**
    
    - **Category:** ConfigurationScript
    
- **Path:** src/scripts/users_permissions/manage_app_users.py  
**Description:** Python script using Pika or the RabbitMQ HTTP API to manage application-specific users, their passwords (securely handled), and their permissions on specific vhosts, exchanges, and queues. This script provides more complex logic or integration possibilities than simple shell scripts.  
**Template:** Python Script  
**Dependency Level:** 1  
**Name:** manage_app_users  
**Type:** UtilityScript  
**Relative Path:** scripts/users_permissions/manage_app_users.py  
**Repository Id:** REPO-RABBITMQ-CONFIGURATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** RABBITMQ_API_URL  
**Type:** str  
**Attributes:** const  
    - **Name:** RABBITMQ_USER  
**Type:** str  
**Attributes:** const  
    - **Name:** RABBITMQ_PASS  
**Type:** str  
**Attributes:** const  
    
**Methods:**
    
    - **Name:** create_user  
**Parameters:**
    
    - username
    - password_hash
    - tags
    
**Return Type:** None  
**Attributes:** static  
    - **Name:** set_permissions  
**Parameters:**
    
    - username
    - vhost
    - configure_regex
    - write_regex
    - read_regex
    
**Return Type:** None  
**Attributes:** static  
    - **Name:** delete_user  
**Parameters:**
    
    - username
    
**Return Type:** None  
**Attributes:** static  
    
**Implemented Features:**
    
    - Application User Management
    - Granular Permission Assignment
    
**Requirement Ids:**
    
    - Section 5.2.2 (Job Queue Management component - implies users for services)
    
**Purpose:** To programmatically manage RabbitMQ users and their permissions using the HTTP API, allowing for more dynamic or complex configurations.  
**Logic Description:** This Python script will use the 'requests' library to interact with the RabbitMQ Management HTTP API. It will include functions to add users (e.g., PUT /api/users/{user}), set permissions (e.g., PUT /api/permissions/{vhost}/{user}), and list/delete users. Usernames, password hashes (if setting directly, or passwords if API hashes), and permission details (configure, write, read regexes for exchanges/queues) will be parameterized or read from a configuration file. This is useful for creating service accounts (e.g., for Odoo, n8n, Notification Service) with specific, least-privilege permissions.  
**Documentation:**
    
    - **Summary:** Python script for managing RabbitMQ users and their permissions via the Management HTTP API. Suitable for creating service accounts with fine-grained access.
    
**Namespace:** N/A  
**Metadata:**
    
    - **Category:** ConfigurationScript
    
- **Path:** src/scripts/cluster_management/check_cluster_status.sh  
**Description:** Shell script using rabbitmqctl to check and report the status of the RabbitMQ cluster, including node health, partitions, and running applications. Useful for operational monitoring and health checks.  
**Template:** Shell Script  
**Dependency Level:** 0  
**Name:** check_cluster_status  
**Type:** UtilityScript  
**Relative Path:** scripts/cluster_management/check_cluster_status.sh  
**Repository Id:** REPO-RABBITMQ-CONFIGURATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** get_cluster_status  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:** function  
    - **Name:** get_node_health  
**Parameters:**
    
    - node_name
    
**Return Type:** void  
**Attributes:** function  
    
**Implemented Features:**
    
    - Cluster Health Monitoring
    
**Requirement Ids:**
    
    - DEP-001 (RabbitMQ Server specs - implies cluster operation)
    
**Purpose:** To provide a quick way to check the overall health and status of the RabbitMQ cluster using rabbitmqctl commands.  
**Logic Description:** This script will execute 'rabbitmqctl cluster_status'. It may parse the output to provide a summarized status or exit with a specific code based on health (e.g., 0 for healthy, 1 for issues). It can also iterate through nodes to check individual node health using 'rabbitmqctl node_health_check <node_name>'. The script can be used in automated health checks or by administrators.  
**Documentation:**
    
    - **Summary:** Shell script to check and report the operational status of a RabbitMQ cluster using rabbitmqctl.
    
**Namespace:** N/A  
**Metadata:**
    
    - **Category:** OperationalScript
    
- **Path:** src/scripts/cluster_management/list_queues_with_counts.py  
**Description:** Python script using Pika or the RabbitMQ HTTP API to list all queues (or queues matching a pattern) along with their current message counts (ready, unacked), consumer counts, and memory usage. Useful for monitoring queue backlog and resource consumption.  
**Template:** Python Script  
**Dependency Level:** 0  
**Name:** list_queues_with_counts  
**Type:** UtilityScript  
**Relative Path:** scripts/cluster_management/list_queues_with_counts.py  
**Repository Id:** REPO-RABBITMQ-CONFIGURATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** RABBITMQ_API_URL  
**Type:** str  
**Attributes:** const  
    - **Name:** RABBITMQ_USER  
**Type:** str  
**Attributes:** const  
    - **Name:** RABBITMQ_PASS  
**Type:** str  
**Attributes:** const  
    
**Methods:**
    
    - **Name:** get_queue_details  
**Parameters:**
    
    - vhost
    - queue_name_pattern
    
**Return Type:** list  
**Attributes:** static  
    
**Implemented Features:**
    
    - Queue Monitoring
    
**Requirement Ids:**
    
    - Section 5.2.2 (Job Queue Management component)
    
**Purpose:** To provide detailed information about queues in the RabbitMQ cluster, including message counts and consumer details, via the HTTP API.  
**Logic Description:** This Python script will use the 'requests' library to call the RabbitMQ Management HTTP API endpoint (e.g., GET /api/queues/{vhost}). It will parse the JSON response to extract queue names, messages_ready, messages_unacknowledged, consumers, and memory. It can accept a vhost and an optional queue name pattern as arguments. The output will be formatted for readability (e.g., table or JSON).  
**Documentation:**
    
    - **Summary:** Python script to list RabbitMQ queues with their message counts, consumer counts, and other relevant statistics, using the Management HTTP API.
    
**Namespace:** N/A  
**Metadata:**
    
    - **Category:** OperationalScript
    
- **Path:** src/requirements.txt  
**Description:** Python dependencies file for any Python scripts in this repository. Primarily for the 'pika' library if direct AMQP interaction is needed, or 'requests' if using the HTTP API.  
**Template:** Python Requirements File  
**Dependency Level:** 0  
**Name:** requirements  
**Type:** DependencyFile  
**Relative Path:** requirements.txt  
**Repository Id:** REPO-RABBITMQ-CONFIGURATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Dependency Management for Python Scripts
    
**Requirement Ids:**
    
    
**Purpose:** To list Python package dependencies required by utility and management scripts within this repository.  
**Logic Description:** This is a standard pip requirements file. It will list packages such as: 
requests==2.x.x  # For RabbitMQ Management HTTP API calls
pika==1.x.x    # For direct AMQP interaction (if used, less likely for pure config repo)  
**Documentation:**
    
    - **Summary:** Specifies Python dependencies for scripts used to manage or interact with RabbitMQ. Ensures reproducible environments for script execution.
    
**Namespace:** N/A  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** src/config/rabbitmq_env.sh.template  
**Description:** Template for environment variables needed by shell scripts to connect to RabbitMQ (e.g., RABBITMQ_CTL_ERLANG_COOKIE, RABBITMQ_NODENAME for remote rabbitmqctl, or API credentials). This file should be copied and filled with actual values, and not committed with secrets.  
**Template:** Shell Script Environment Template  
**Dependency Level:** 0  
**Name:** rabbitmq_env.sh.template  
**Type:** ConfigurationTemplate  
**Relative Path:** config/rabbitmq_env.sh.template  
**Repository Id:** REPO-RABBITMQ-CONFIGURATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Secure Configuration Management
    
**Requirement Ids:**
    
    
**Purpose:** To provide a template for setting up environment variables required by shell scripts to interact with RabbitMQ, promoting secure handling of credentials.  
**Logic Description:** This file will contain lines like:
export RABBITMQ_USER="your_admin_user"
export RABBITMQ_PASS="your_admin_password"
export RABBITMQ_MANAGEMENT_URL="http://localhost:15672"
export RABBITMQ_DEFAULT_VHOST="/"
It will instruct the user to copy it to 'rabbitmq_env.sh' (which should be in .gitignore if secrets are present) and populate the actual values.  
**Documentation:**
    
    - **Summary:** A template file for setting environment variables needed by RabbitMQ management scripts, such as connection details and credentials.
    
**Namespace:** N/A  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** src/config/rabbitmq_api_client_config.py.template  
**Description:** Template for Python configuration providing credentials and endpoint for the RabbitMQ Management HTTP API, used by Python management scripts. This file should be copied and filled, and not committed with secrets.  
**Template:** Python Configuration Template  
**Dependency Level:** 0  
**Name:** rabbitmq_api_client_config.py.template  
**Type:** ConfigurationTemplate  
**Relative Path:** config/rabbitmq_api_client_config.py.template  
**Repository Id:** REPO-RABBITMQ-CONFIGURATION-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Secure Configuration Management
    
**Requirement Ids:**
    
    
**Purpose:** To provide a template for Python script configurations, storing RabbitMQ Management API connection details and credentials securely.  
**Logic Description:** This file will define Python variables or a dictionary:
# Copy to rabbitmq_api_client_config.py and fill in your details
# Ensure rabbitmq_api_client_config.py is in .gitignore
RABBITMQ_API_CONFIG = {
    'url': 'http://localhost:15672',
    'username': 'your_admin_user',
    'password': 'your_admin_password',
    'default_vhost': '/'
}
Python scripts will then import this configuration.  
**Documentation:**
    
    - **Summary:** Template for Python configuration file containing RabbitMQ Management HTTP API endpoint and credentials.
    
**Namespace:** N/A  
**Metadata:**
    
    - **Category:** Configuration
    


---

# 2. Configuration

- **Feature Toggles:**
  
  
- **Database Configs:**
  
  


---

