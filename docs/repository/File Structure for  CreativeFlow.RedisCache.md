# Specification

# 1. Files

- **Path:** conf/redis.conf.tpl  
**Description:** Master template for Redis server configuration. Includes settings for port, bind address, persistence (RDB/AOF), memory limits, security (requirepass, protected-mode), client connection limits, basic Pub/Sub event notifications, and eviction policies relevant for session management and caching. Placeholders are used for environment-specific values to be injected by configuration management tools like Ansible.  
**Template:** Redis Configuration Template  
**Dependency Level:** 0  
**Name:** redis.conf  
**Type:** Configuration  
**Relative Path:** conf/redis.conf.tpl  
**Repository Id:** REPO-REDIS-CACHE-001  
**Pattern Ids:**
    
    - ConfigurationTemplate
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Redis Server Configuration
    - Persistence Configuration (RDB/AOF)
    - Security Settings (Password, Bind)
    - Memory Management Policies
    - Session Management Support Configuration
    - Caching Strategy Configuration
    - Pub/Sub Basic Configuration
    
**Requirement Ids:**
    
    - Section 5.1 (Redis in Arch)
    - Section 5.2.2 (Caching component)
    - SEC-002 (Session management)
    - DEP-001 (Redis Server specs)
    
**Purpose:** Provides a templated base configuration for Redis server instances, ensuring consistency and adherence to security and performance best practices.  
**Logic Description:** This file contains Redis configuration directives with placeholders for dynamic values. Key sections cover: General (port, bind, protected-mode, daemonize, pidfile, logfile, databases), Snapshots (save points, dbfilename, rdbcompression), Append Only Mode (appendonly, appendfsync), Security (requirepass), Clients (maxclients), Memory Management (maxmemory, maxmemory-policy), Event Notification (notify-keyspace-events). It should be configured to align with server specifications from DEP-001 and support SEC-002 for session data.  
**Documentation:**
    
    - **Summary:** Redis server configuration template. Defines how Redis instances behave regarding networking, persistence, security, and resource usage.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** conf/sentinel.conf.tpl  
**Description:** Template for Redis Sentinel configuration. Used for setting up Redis High Availability by monitoring master and replica instances, and managing automatic failover. Placeholders are used for environment-specific values.  
**Template:** Redis Configuration Template  
**Dependency Level:** 0  
**Name:** sentinel.conf  
**Type:** Configuration  
**Relative Path:** conf/sentinel.conf.tpl  
**Repository Id:** REPO-REDIS-CACHE-001  
**Pattern Ids:**
    
    - ConfigurationTemplate
    - HighAvailability
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Redis Sentinel Configuration
    - High Availability Setup
    
**Requirement Ids:**
    
    - Section 5.1 (Redis in Arch)
    - Section 5.2.2 (Caching component)
    - DEP-001 (Redis Server specs)
    
**Purpose:** Provides a templated base configuration for Redis Sentinel instances, enabling high availability for Redis master-replica setups.  
**Logic Description:** This file contains Redis Sentinel configuration directives. Key placeholders include: port, sentinel monitor <master-name> <ip> <port> <quorum>, sentinel down-after-milliseconds <master-name> <milliseconds>, sentinel parallel-syncs <master-name> <numslaves>, sentinel failover-timeout <master-name> <milliseconds>, and sentinel auth-pass <master-name> <password> if the master is password-protected. This configuration directly supports the HA aspect of DEP-001.  
**Documentation:**
    
    - **Summary:** Redis Sentinel configuration template. Defines how Sentinel nodes monitor Redis masters and handle failovers.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** scripts/common_env.sh  
**Description:** Common environment variables and utility functions for shell scripts in this repository. Defines default paths, Redis CLI locations, or shared helper functions for script consistency.  
**Template:** Shell Script  
**Dependency Level:** 0  
**Name:** common_env  
**Type:** Utility  
**Relative Path:** scripts/common_env.sh  
**Repository Id:** REPO-REDIS-CACHE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Shared Script Configuration
    - Utility Functions for Scripts
    
**Requirement Ids:**
    
    
**Purpose:** Centralizes common settings and helper functions for shell scripts to improve maintainability and consistency.  
**Logic Description:** Defines environment variables such as REDIS_CLI_PATH, DEFAULT_REDIS_HOST, DEFAULT_REDIS_PORT. May include shell functions for logging, error handling, or executing common Redis CLI commands with consistent options. This script is sourced by other operational scripts.  
**Documentation:**
    
    - **Summary:** Provides shared environment settings and utility functions for operational shell scripts.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** OperationalScript
    
- **Path:** scripts/manage_redis_server.sh  
**Description:** Shell script to start, stop, restart, and check the status of a Redis server instance. Takes configuration file and PID file paths as arguments. Interacts with the Redis server executable and redis-cli.  
**Template:** Shell Script  
**Dependency Level:** 1  
**Name:** manage_redis_server  
**Type:** OperationalScript  
**Relative Path:** scripts/manage_redis_server.sh  
**Repository Id:** REPO-REDIS-CACHE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Redis Server Lifecycle Management (Start, Stop, Restart, Status)
    
**Requirement Ids:**
    
    - DEP-001 (Redis Server specs)
    
**Purpose:** Automates common lifecycle operations for a single Redis server instance.  
**Logic Description:** Script accepts actions like 'start', 'stop', 'restart', 'status'. Uses 'redis-server <config_file>' to start. Uses 'redis-cli -p <port> [-a <password>] SHUTDOWN' or signals to stop. Checks status using 'redis-cli -p <port> [-a <password>] PING'. Sources 'common_env.sh' for defaults. Manages PID file.  
**Documentation:**
    
    - **Summary:** Manages the lifecycle of a Redis server instance. Inputs: action (start|stop|restart|status), config_file_path, pid_file_path. Outputs: Status messages.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** OperationalScript
    
- **Path:** scripts/manage_sentinel.sh  
**Description:** Shell script to start, stop, restart, and check the status of a Redis Sentinel instance. Takes Sentinel configuration file and PID file paths as arguments. Interacts with the redis-sentinel executable.  
**Template:** Shell Script  
**Dependency Level:** 1  
**Name:** manage_sentinel  
**Type:** OperationalScript  
**Relative Path:** scripts/manage_sentinel.sh  
**Repository Id:** REPO-REDIS-CACHE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Redis Sentinel Lifecycle Management (Start, Stop, Restart, Status)
    
**Requirement Ids:**
    
    - DEP-001 (Redis Server specs)
    
**Purpose:** Automates common lifecycle operations for a single Redis Sentinel instance, crucial for HA.  
**Logic Description:** Script accepts actions like 'start', 'stop', 'restart', 'status'. Uses 'redis-sentinel <config_file>' or 'redis-server <config_file> --sentinel' to start. Uses signals or 'redis-cli -p <sentinel_port> SHUTDOWN' to stop. Checks status via PID file or PING to Sentinel port. Sources 'common_env.sh'. Manages PID file.  
**Documentation:**
    
    - **Summary:** Manages the lifecycle of a Redis Sentinel instance. Inputs: action (start|stop|restart|status), config_file_path, pid_file_path. Outputs: Status messages.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** OperationalScript
    
- **Path:** scripts/monitoring/check_redis_health.py  
**Description:** Python script for performing comprehensive health checks on Redis instances and Sentinel setup. Gathers key metrics related to performance, memory, replication, and client connections. Output suitable for monitoring systems.  
**Template:** Python Script  
**Dependency Level:** 1  
**Name:** check_redis_health  
**Type:** OperationalScript  
**Relative Path:** scripts/monitoring/check_redis_health.py  
**Repository Id:** REPO-REDIS-CACHE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** main  
**Parameters:**
    
    - args
    
**Return Type:** None  
**Attributes:**   
    - **Name:** get_redis_connection  
**Parameters:**
    
    - host
    - port
    - password=None
    
**Return Type:** redis.Redis  
**Attributes:** private  
    - **Name:** check_instance_liveness  
**Parameters:**
    
    - client
    
**Return Type:** dict  
**Attributes:** private  
    - **Name:** get_instance_info  
**Parameters:**
    
    - client
    - sections=['default']
    
**Return Type:** dict  
**Attributes:** private  
    - **Name:** check_replication_status  
**Parameters:**
    
    - client
    
**Return Type:** dict  
**Attributes:** private  
    - **Name:** check_sentinel_status  
**Parameters:**
    
    - sentinel_host
    - sentinel_port
    - master_name
    
**Return Type:** dict  
**Attributes:** private  
    
**Implemented Features:**
    
    - Redis Health Monitoring
    - Sentinel Status Check
    - Replication Lag Monitoring
    - Key Metric Collection
    
**Requirement Ids:**
    
    - Section 5.2.2 (Caching component)
    
**Purpose:** Provides detailed health status and key metrics for Redis instances and Sentinel setup, aiding in operational monitoring and troubleshooting.  
**Logic Description:** Uses 'redis-py' library. Parses command-line arguments for connection details (host, port, password, Sentinel info). Connects to Redis/Sentinel. Executes 'PING', 'INFO ALL', 'ROLE', 'SENTINEL MASTER <master_name>', 'SENTINEL SLAVES <master_name>' commands. Parses output to extract metrics like uptime, connected_clients, used_memory, instantaneous_ops_per_sec, master/slave status, replication lag, number of sentinels, quorum status. Outputs results in JSON or Nagios-compatible format.  
**Documentation:**
    
    - **Summary:** Python script for Redis and Sentinel health checks. Inputs: Redis/Sentinel connection parameters. Outputs: Health status and metrics in a structured format.
    
**Namespace:** CreativeFlow.Data.Redis.Monitoring  
**Metadata:**
    
    - **Category:** OperationalScript
    
- **Path:** python_utils/__init__.py  
**Description:** Makes the python_utils directory a Python package.  
**Template:** Python Script  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** python_utils/__init__.py  
**Repository Id:** REPO-REDIS-CACHE-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the python_utils directory as a Python package, allowing modules within it to be imported.  
**Logic Description:** This file can be empty or can be used to expose specific functions/classes from modules within the package at the package level.  
**Documentation:**
    
    - **Summary:** Python package initializer for the python_utils directory.
    
**Namespace:** CreativeFlow.Data.Redis.PythonUtils  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** python_utils/redis_connector.py  
**Description:** Centralized module for creating and managing Redis connections for other Python scripts in this repository.  
**Template:** Python Script  
**Dependency Level:** 0  
**Name:** redis_connector  
**Type:** Utility  
**Relative Path:** python_utils/redis_connector.py  
**Repository Id:** REPO-REDIS-CACHE-001  
**Pattern Ids:**
    
    - Singleton (optional for connection pool)
    
**Members:**
    
    - **Name:** connection_pool  
**Type:** redis.ConnectionPool  
**Attributes:** private|static  
    
**Methods:**
    
    - **Name:** get_redis_connection  
**Parameters:**
    
    - host='localhost'
    - port=6379
    - password=None
    - db=0
    - use_pool=True
    
**Return Type:** redis.Redis  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - Reusable Redis Connection Logic
    
**Requirement Ids:**
    
    
**Purpose:** Provides a consistent way for other Python scripts within this repository to establish connections to Redis.  
**Logic Description:** Uses 'redis-py'. Implements a function `get_redis_connection` that takes connection parameters and returns a `redis.Redis` client instance. May optionally implement a connection pool for efficiency if scripts make frequent connections. Handles basic error checking for connection establishment.  
**Documentation:**
    
    - **Summary:** Module for establishing Redis connections. Provides a reusable function to get a Redis client.
    
**Namespace:** CreativeFlow.Data.Redis.PythonUtils  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** python_utils/session_utils.py  
**Description:** Python utility module providing functions for administrative or diagnostic tasks related to user sessions stored in Redis. Not for application-level session handling.  
**Template:** Python Script  
**Dependency Level:** 1  
**Name:** session_utils  
**Type:** Utility  
**Relative Path:** python_utils/session_utils.py  
**Repository Id:** REPO-REDIS-CACHE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** redis_client  
**Type:** redis.Redis  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - redis_client
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** count_active_sessions  
**Parameters:**
    
    - session_key_prefix='session:'
    
**Return Type:** int  
**Attributes:** public  
    - **Name:** get_session_details  
**Parameters:**
    
    - session_id
    
**Return Type:** dict  
**Attributes:** public  
    - **Name:** list_sessions_by_pattern  
**Parameters:**
    
    - pattern
    
**Return Type:** list  
**Attributes:** public  
    - **Name:** clear_session  
**Parameters:**
    
    - session_id
    
**Return Type:** bool  
**Attributes:** public  
    
**Implemented Features:**
    
    - Session Data Inspection
    - Session Data Management (Admin)
    
**Requirement Ids:**
    
    - SEC-002 (Session management using Redis)
    
**Purpose:** Offers tools for administrators to inspect, count, or clear user sessions stored in Redis for debugging or operational needs.  
**Logic Description:** Uses 'redis-py' via the `redis_connector`. Class `SessionAdminTools` with methods. `count_active_sessions` uses `SCAN` or `KEYS` (with caution on production) with a prefix. `get_session_details` fetches and potentially decodes session data. `list_sessions_by_pattern` helps find specific sessions. `clear_session` deletes a specific session key. These are for direct admin intervention, not regular app flow.  
**Documentation:**
    
    - **Summary:** Administrative utilities for managing Redis sessions. Provides functions for inspecting and clearing session data.
    
**Namespace:** CreativeFlow.Data.Redis.PythonUtils  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** python_utils/cache_admin_tools.py  
**Description:** Python utility module for administrative tasks related to managing general-purpose caches in Redis, such as templates or user preferences.  
**Template:** Python Script  
**Dependency Level:** 1  
**Name:** cache_admin_tools  
**Type:** Utility  
**Relative Path:** python_utils/cache_admin_tools.py  
**Repository Id:** REPO-REDIS-CACHE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** redis_client  
**Type:** redis.Redis  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - redis_client
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** list_cache_keys  
**Parameters:**
    
    - pattern='cache:*'
    
**Return Type:** list  
**Attributes:** public  
    - **Name:** get_cache_value  
**Parameters:**
    
    - key
    
**Return Type:** any  
**Attributes:** public  
    - **Name:** get_cache_ttl  
**Parameters:**
    
    - key
    
**Return Type:** int  
**Attributes:** public  
    - **Name:** delete_cache_key  
**Parameters:**
    
    - key
    
**Return Type:** bool  
**Attributes:** public  
    - **Name:** flush_cache_by_pattern  
**Parameters:**
    
    - pattern
    
**Return Type:** int  
**Attributes:** public  
    
**Implemented Features:**
    
    - Cache Inspection
    - Cache Key Deletion
    - Cache TTL Check
    
**Requirement Ids:**
    
    - Section 5.2.2 (Caching component as Redis)
    
**Purpose:** Provides tools for administrators to inspect, manage, and clear cached items in Redis for operational and debugging purposes.  
**Logic Description:** Uses 'redis-py' via `redis_connector`. Class `CacheAdmin` with methods. `list_cache_keys` uses `SCAN` for pattern matching. `get_cache_value` retrieves and potentially deserializes cached data. `get_cache_ttl` gets the time-to-live for a key. `delete_cache_key` removes a specific key. `flush_cache_by_pattern` deletes multiple keys matching a pattern.  
**Documentation:**
    
    - **Summary:** Administrative utilities for managing general caches in Redis. Provides functions for listing, viewing, and deleting cache entries.
    
**Namespace:** CreativeFlow.Data.Redis.PythonUtils  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** python_utils/rate_limit_utils.py  
**Description:** Python utility module for inspecting or managing rate limit counters stored in Redis. For operational monitoring and potential manual adjustments by administrators.  
**Template:** Python Script  
**Dependency Level:** 1  
**Name:** rate_limit_utils  
**Type:** Utility  
**Relative Path:** python_utils/rate_limit_utils.py  
**Repository Id:** REPO-REDIS-CACHE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** redis_client  
**Type:** redis.Redis  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - redis_client
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** get_rate_limit_value  
**Parameters:**
    
    - counter_key
    
**Return Type:** int  
**Attributes:** public  
    - **Name:** reset_rate_limit_counter  
**Parameters:**
    
    - counter_key
    
**Return Type:** bool  
**Attributes:** public  
    - **Name:** list_rate_limit_keys  
**Parameters:**
    
    - pattern='ratelimit:*'
    
**Return Type:** list  
**Attributes:** public  
    
**Implemented Features:**
    
    - Rate Limit Counter Inspection
    - Rate Limit Counter Reset (Admin)
    
**Requirement Ids:**
    
    - Section 5.2.2 (Caching component as Redis)
    
**Purpose:** Provides tools for administrators to monitor and manage rate limit counters stored in Redis, aiding in operational oversight.  
**Logic Description:** Uses 'redis-py' via `redis_connector`. Class `RateLimitAdmin` with methods. `get_rate_limit_value` fetches the current value of a rate limit counter. `reset_rate_limit_counter` sets a counter back to 0 or deletes it. `list_rate_limit_keys` uses `SCAN` to find active rate limit keys.  
**Documentation:**
    
    - **Summary:** Administrative utilities for rate limit counters in Redis. Allows viewing and resetting rate limit values.
    
**Namespace:** CreativeFlow.Data.Redis.PythonUtils  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** python_utils/pubsub_diagnostics.py  
**Description:** Python utility module for diagnosing the Pub/Sub mechanism in Redis, primarily used by the Notification Service. Allows inspection of channels and subscriber counts.  
**Template:** Python Script  
**Dependency Level:** 1  
**Name:** pubsub_diagnostics  
**Type:** Utility  
**Relative Path:** python_utils/pubsub_diagnostics.py  
**Repository Id:** REPO-REDIS-CACHE-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** redis_client  
**Type:** redis.Redis  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - redis_client
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** list_active_channels  
**Parameters:**
    
    - pattern='*'
    
**Return Type:** list  
**Attributes:** public  
    - **Name:** get_channel_subscriber_count  
**Parameters:**
    
    - channel_name
    
**Return Type:** int  
**Attributes:** public  
    - **Name:** publish_test_message  
**Parameters:**
    
    - channel_name
    - message
    
**Return Type:** int  
**Attributes:** public  
    
**Implemented Features:**
    
    - Pub/Sub Channel Inspection
    - Pub/Sub Subscriber Count
    - Test Message Publishing
    
**Requirement Ids:**
    
    - Section 5.2.2 (Caching component as Redis)
    
**Purpose:** Provides diagnostic tools for administrators to monitor the health and activity of Redis Pub/Sub channels.  
**Logic Description:** Uses 'redis-py' via `redis_connector`. Class `PubSubAdmin` with methods. `list_active_channels` uses `PUBSUB CHANNELS [pattern]`. `get_channel_subscriber_count` uses `PUBSUB NUMSUB [channel ...]`. `publish_test_message` uses `PUBLISH` to send a diagnostic message to a channel.  
**Documentation:**
    
    - **Summary:** Diagnostic utilities for Redis Pub/Sub. Allows listing channels, checking subscriber counts, and publishing test messages.
    
**Namespace:** CreativeFlow.Data.Redis.PythonUtils  
**Metadata:**
    
    - **Category:** Utility
    


---

# 2. Configuration

- **Feature Toggles:**
  
  
- **Database Configs:**
  
  - REDIS_HOST
  - REDIS_PORT
  - REDIS_PASSWORD
  - REDIS_SESSION_DB_INDEX
  - REDIS_CACHE_DB_INDEX
  - REDIS_PUBSUB_DB_INDEX
  - SENTINEL_HOSTS
  - SENTINEL_MASTER_NAME
  - SENTINEL_PASSWORD
  


---

