# Software Design Specification: CreativeFlow.RedisCache

## 1. Introduction

### 1.1 Purpose
This document provides the Software Design Specification (SDS) for the `CreativeFlow.RedisCache` repository. This repository is responsible for the configuration templates and operational scripts for the Redis in-memory data store within the CreativeFlow AI platform. Redis serves critical functions including session management, content caching, rate limiting, and as a Pub/Sub mechanism for the Notification Service.

### 1.2 Scope
This SDS covers:
*   Configuration templates for Redis server (`redis.conf.tpl`) and Redis Sentinel (`sentinel.conf.tpl`).
*   Shell scripts for managing Redis server and Sentinel instances.
*   Python scripts for monitoring Redis health and administrative utilities for managing sessions, caches, rate limiters, and Pub/Sub diagnostics.
*   Design considerations for high availability, persistence, security, and memory management.

### 1.3 Definitions, Acronyms, and Abbreviations
*   **Redis**: Remote Dictionary Server, an in-memory data structure store.
*   **Sentinel**: Redis high availability solution.
*   **RDB**: Redis Database Backup, a persistence mechanism.
*   **AOF**: Append Only File, another persistence mechanism for Redis.
*   **Pub/Sub**: Publish/Subscribe messaging paradigm.
*   **HA**: High Availability.
*   **SDS**: Software Design Specification.
*   **CLI**: Command Line Interface.
*   **PWA**: Progressive Web Application.
*   **API**: Application Programming Interface.
*   **PID**: Process ID.
*   **CI/CD**: Continuous Integration / Continuous Deployment.
*   **KMS**: Key Management Service.
*   **IaC**: Infrastructure as Code.
*   **Ansible**: IT automation tool.
*   **TTL**: Time To Live.

## 2. System Overview
The `CreativeFlow.RedisCache` component provides the foundational configuration and operational tooling for the Redis instances within the CreativeFlow AI platform. Redis is a critical component for:
*   **Session Management (SEC-002)**: Storing active user sessions for both web and mobile applications, enabling fast retrieval and validation.
*   **Content Caching (Section 5.2.2)**: Caching frequently accessed data such as resolved templates, user preferences, and other static or semi-static content to reduce database load and improve response times.
*   **Rate Limiting Counters (Section 5.2.2)**: Maintaining counters for API rate limiting and other usage-based controls.
*   **Pub/Sub Mechanism (Section 5.2.2)**: Facilitating real-time communication by acting as a message bus for the Notification Service, propagating events to connected clients.

The system is designed for high availability using Redis Sentinel and supports configurable persistence mechanisms (RDB and AOF) to ensure data durability according to operational needs. Security is addressed through password protection and network binding. Configuration will be managed via Ansible, leveraging the templates provided in this repository.

## 3. Design Considerations

### 3.1 High Availability
*   Redis Sentinel will be used to monitor Redis master and replica instances.
*   Automatic failover will be configured to promote a replica to master in case the primary master becomes unavailable.
*   A minimum quorum will be defined for Sentinel nodes to make decisions, ensuring reliability of the failover process.
*   Configuration templates (`sentinel.conf.tpl`) will support these HA setups.

### 3.2 Persistence
*   Both RDB snapshots and AOF (Append Only File) persistence options will be configurable via `redis.conf.tpl`.
*   **RDB Snapshots**: Provides point-in-time backups. Configuration will allow defining snapshotting frequency (e.g., `save 900 1`, `save 300 10`, `save 60 10000`).
*   **AOF Persistence**: Logs every write operation received by the server. `appendfsync` policy (e.g., `everysec`, `always`) will be configurable to balance durability and performance.
*   The choice and tuning of persistence mechanisms will depend on the specific data stored in each Redis instance/database (e.g., sessions might tolerate less stringent persistence than critical cached data if it can be rebuilt).

### 3.3 Security
*   **Password Protection**: Redis instances will be secured with a strong password using the `requirepass` directive in `redis.conf.tpl`. Sentinel nodes will also be configured with `sentinel auth-pass` if the master is password-protected.
*   **Network Binding**: Redis instances will be configured to bind to specific private network interfaces (`bind` directive) rather than all interfaces (`0.0.0.0`), limiting accessibility.
*   **Protected Mode**: `protected-mode yes` will be the default to prevent access from untrusted clients if no password is set or explicit bind is not used.
*   Regular OS and Redis software patching will be part of the operational procedures (managed by Ansible).

### 3.4 Memory Management
*   `maxmemory` directive will be used to set an upper limit on memory usage for Redis instances, preventing excessive consumption.
*   `maxmemory-policy` (e.g., `allkeys-lru`, `volatile-lru`, `allkeys-random`) will be configured based on the use case of the Redis instance (e.g., LRU for caches, potentially different for session stores).
*   Server specifications from `DEP-001` will guide the `maxmemory` settings.

### 3.5 Separation of Concerns (Redis Databases)
To isolate different types of data and manage them effectively, distinct Redis logical databases (selectable via `SELECT <db_index>`) will be used for:
*   User Sessions (e.g., DB 0)
*   Application Cache (e.g., DB 1)
*   Pub/Sub related data (if any persistent state is needed beyond message passing) (e.g., DB 2)
*   Rate Limiting Counters (e.g., DB 3)
This allows for different persistence, eviction, or security policies per database if required, though Redis configuration is typically instance-wide for persistence and memory.

## 4. Configuration Files Specification

### 4.1 `conf/redis.conf.tpl`
*   **Purpose**: Master template for Redis server configuration, enabling consistent and customizable deployment of Redis instances.
*   **Key Configuration Sections and Parameters**:
    *   **General**:
        *   `port {{ REDIS_PORT | default(6379) }}`
        *   `bind {{ REDIS_BIND_IP | default("127.0.0.1") }}` (Ansible should set this to the server's private IP)
        *   `protected-mode {{ REDIS_PROTECTED_MODE | default("yes") }}`
        *   `daemonize {{ REDIS_DAEMONIZE | default("yes") }}`
        *   `pidfile /var/run/redis/redis_server_{{ REDIS_PORT | default(6379) }}.pid`
        *   `logfile /var/log/redis/redis_server_{{ REDIS_PORT | default(6379) }}.log`
        *   `databases {{ REDIS_DATABASES | default(16) }}`
    *   **Snapshots (RDB)**:
        *   `save 900 1`
        *   `save 300 10`
        *   `save 60 10000`
        *   `dbfilename dump_{{ REDIS_PORT | default(6379) }}.rdb`
        *   `rdbcompression {{ REDIS_RDB_COMPRESSION | default("yes") }}`
        *   `dir /var/lib/redis/{{ REDIS_PORT | default(6379) }}`
    *   **Append Only Mode (AOF)**:
        *   `appendonly {{ REDIS_AOF_ENABLED | default("no") }}` (Consider 'yes' for higher durability needs)
        *   `appendfilename "appendonly_{{ REDIS_PORT | default(6379) }}.aof"`
        *   `appendfsync {{ REDIS_AOF_FSYNC_POLICY | default("everysec") }}`
    *   **Security**:
        *   `requirepass {{ REDIS_PASSWORD }}` (Placeholder: Ansible must inject this from a secure vault)
    *   **Clients**:
        *   `maxclients {{ REDIS_MAX_CLIENTS | default(10000) }}`
    *   **Memory Management**:
        *   `maxmemory {{ REDIS_MAX_MEMORY }}` (Placeholder: Ansible injects based on DEP-001)
        *   `maxmemory-policy {{ REDIS_MAXMEMORY_POLICY | default("allkeys-lru") }}`
    *   **Event Notification (Keyspace Notifications for Pub/Sub and Monitoring)**:
        *   `notify-keyspace-events {{ REDIS_KEYSPACE_EVENTS | default("KEA") }}` (KEA = Keyspace, Expired, All events. Adjust as needed for specific features like session expiration notifications or cache invalidation.)
*   **Placeholder Variables**: Indicated by `{{ VARIABLE_NAME }}`. These will be replaced by Ansible during deployment.
*   **Relation to Requirements**:
    *   `Section 5.1`, `Section 5.2.2`: Defines the core Redis server behavior.
    *   `SEC-002`: `maxmemory`, `maxmemory-policy` and persistence settings are relevant for session data. `requirepass` and `bind` for security.
    *   `DEP-001`: `maxmemory`, `port`, `dir` should align with server specifications.

### 4.2 `conf/sentinel.conf.tpl`
*   **Purpose**: Template for Redis Sentinel configuration, facilitating the setup of high-availability Redis clusters.
*   **Key Configuration Sections and Parameters**:
    *   `port {{ SENTINEL_PORT | default(26379) }}`
    *   `daemonize {{ SENTINEL_DAEMONIZE | default("yes") }}`
    *   `pidfile /var/run/redis/sentinel_{{ SENTINEL_PORT | default(26379) }}.pid`
    *   `logfile /var/log/redis/sentinel_{{ SENTINEL_PORT | default(26379) }}.log`
    *   `dir /tmp` (or a persistent directory if Sentinel state needs to be preserved across restarts for some reason, though typically Sentinel discovers state dynamically)
    *   `sentinel monitor {{ SENTINEL_MASTER_NAME }} {{ SENTINEL_MASTER_IP }} {{ SENTINEL_MASTER_PORT }} {{ SENTINEL_QUORUM }}`
    *   `sentinel down-after-milliseconds {{ SENTINEL_MASTER_NAME }} {{ SENTINEL_DOWN_AFTER_MS | default(30000) }}`
    *   `sentinel parallel-syncs {{ SENTINEL_MASTER_NAME }} {{ SENTINEL_PARALLEL_SYNCS | default(1) }}`
    *   `sentinel failover-timeout {{ SENTINEL_MASTER_NAME }} {{ SENTINEL_FAILOVER_TIMEOUT | default(180000) }}`
    *   `{% if SENTINEL_MASTER_PASSWORD %}`
    *   `sentinel auth-pass {{ SENTINEL_MASTER_NAME }} {{ SENTINEL_MASTER_PASSWORD }}`
    *   `{% endif %}`
    *   `{% if SENTINEL_PASSWORD %}`
    *   `requirepass {{ SENTINEL_PASSWORD }}` (Password for Sentinel itself)
    *   `sentinel sentinel-user {{ SENTINEL_USER | default("default") }} password {{ SENTINEL_PASSWORD }} +all`
    *   `{% endif %}`
*   **Placeholder Variables**: Indicated by `{{ VARIABLE_NAME }}`. Ansible will manage these.
*   **Relation to Requirements**:
    *   `Section 5.1`, `Section 5.2.2`: Defines Sentinel behavior for HA.
    *   `DEP-001`: Ensures Redis setup adheres to HA infrastructure requirements.

## 5. Operational Scripts Specification

### 5.1 `scripts/common_env.sh`
*   **Purpose**: Centralizes common environment variables and utility functions for shell scripts within this repository.
*   **Key Environment Variables**:
    bash
    #!/bin/bash
    # Common Environment Variables
    REDIS_CLI_PATH=$(which redis-cli || echo "/usr/local/bin/redis-cli") # Attempt to find redis-cli, fallback to a common path
    DEFAULT_REDIS_HOST="127.0.0.1"
    # DEFAULT_REDIS_PORT will be passed as an argument or set specifically by calling scripts
    # DEFAULT_REDIS_PASSWORD will be passed as an argument if needed

    # Logging Functions
    log_info() {
        echo "[INFO] $(date +'%Y-%m-%d %H:%M:%S') - $1"
    }

    log_error() {
        echo "[ERROR] $(date +'%Y-%m-%d %H:%M:%S') - $1" >&2
    }

    check_command_exists() {
        command -v "$1" >/dev/null 2>&1 || { log_error "Command '$1' not found. Please install it or check PATH."; exit 1; }
    }
    
*   **Utility Functions**:
    *   `log_info(message)`: Standardized informational logging.
    *   `log_error(message)`: Standardized error logging.
    *   `check_command_exists(command_name)`: Verifies if a command is available in PATH.

### 5.2 `scripts/manage_redis_server.sh`
*   **Purpose**: Automates start, stop, restart, and status check operations for a Redis server instance.
*   **Supported Actions**: `start`, `stop`, `restart`, `status`.
*   **Input Parameters**:
    1.  `ACTION`: The operation to perform (start|stop|restart|status).
    2.  `CONFIG_FILE`: Absolute path to the Redis configuration file (`redis.conf`).
    3.  `PID_FILE`: Absolute path to the Redis PID file.
    4.  `PORT`: (Optional) Redis port, defaults to parsing from config or 6379.
    5.  `PASSWORD`: (Optional) Redis password for shutdown/ping, if `requirepass` is set.
*   **Output**: Status messages to STDOUT/STDERR.
*   **Key Logic**:
    *   Sources `scripts/common_env.sh`.
    *   `start`:
        *   Checks if server is already running (via PID file or PING).
        *   Executes `redis-server $CONFIG_FILE`.
        *   Verifies startup by checking PID file creation and PING.
    *   `stop`:
        *   Reads PID from `$PID_FILE`.
        *   Sends `SHUTDOWN` command via `redis-cli -p $PORT [-a $PASSWORD] SHUTDOWN SAVE` (to ensure persistence). If graceful shutdown fails, uses `kill <PID>`.
        *   Verifies shutdown.
    *   `restart`: Executes `stop` then `start`.
    *   `status`:
        *   Checks if PID file exists and process is running.
        *   Performs `redis-cli -p $PORT [-a $PASSWORD] PING`. Reports "PONG" as running, or error.
*   **Dependencies**: `redis-server`, `redis-cli`.

### 5.3 `scripts/manage_sentinel.sh`
*   **Purpose**: Automates start, stop, restart, and status check operations for a Redis Sentinel instance.
*   **Supported Actions**: `start`, `stop`, `restart`, `status`.
*   **Input Parameters**:
    1.  `ACTION`: The operation to perform (start|stop|restart|status).
    2.  `CONFIG_FILE`: Absolute path to the Sentinel configuration file (`sentinel.conf`).
    3.  `PID_FILE`: Absolute path to the Sentinel PID file.
    4.  `PORT`: (Optional) Sentinel port, defaults to parsing from config or 26379.
    5.  `PASSWORD`: (Optional) Sentinel password for shutdown/ping, if `requirepass` is set for Sentinel.
*   **Output**: Status messages to STDOUT/STDERR.
*   **Key Logic**:
    *   Sources `scripts/common_env.sh`.
    *   `start`:
        *   Checks if Sentinel is already running.
        *   Executes `redis-sentinel $CONFIG_FILE` or `redis-server $CONFIG_FILE --sentinel`.
        *   Verifies startup.
    *   `stop`:
        *   Reads PID from `$PID_FILE`.
        *   Sends `SHUTDOWN` command via `redis-cli -p $PORT [-a $PASSWORD] SHUTDOWN` or uses `kill <PID>`.
        *   Verifies shutdown.
    *   `restart`: Executes `stop` then `start`.
    *   `status`:
        *   Checks if PID file exists and process is running.
        *   Performs `redis-cli -p $PORT [-a $PASSWORD] PING`. Reports "PONG" as running.
*   **Dependencies**: `redis-sentinel` (or `redis-server --sentinel`), `redis-cli`.

### 5.4 `scripts/monitoring/check_redis_health.py`
*   **Purpose**: Performs comprehensive health checks on Redis instances (master/replica) and Sentinel setup, outputting key metrics.
*   **Libraries**: `redis` (redis-py), `argparse`, `json`, `sys`.
*   **Input Parameters (via command-line arguments)**:
    *   `--host`: Redis server host (default: `localhost`).
    *   `--port`: Redis server port (default: `6379`).
    *   `--password`: Redis server password (optional).
    *   `--sentinel-host`: Sentinel host (optional, if checking Sentinel).
    *   `--sentinel-port`: Sentinel port (optional, default: `26379`).
    *   `--sentinel-master-name`: Name of the master monitored by Sentinel (required if checking Sentinel).
    *   `--sentinel-password`: Sentinel password (optional).
    *   `--output-format`: `json` or `nagios` (default: `json`).
*   **Output**: Health status and metrics in JSON or Nagios-compatible format.
*   **Class/Method Structure**:
    python
    import redis
    import argparse
    import json
    import sys
    import time

    class RedisHealthChecker:
        def __init__(self, host, port, password=None):
            self.host = host
            self.port = int(port)
            self.password = password
            self.client = None

        def _get_redis_connection(self):
            """Establishes and returns a Redis connection."""
            if self.client and self.client.ping():
                return self.client
            try:
                self.client = redis.Redis(host=self.host, port=self.port, password=self.password,
                                          socket_connect_timeout=2, socket_timeout=2, decode_responses=True)
                self.client.ping()
                return self.client
            except redis.exceptions.ConnectionError as e:
                # print(f"Error connecting to Redis at {self.host}:{self.port}: {e}", file=sys.stderr)
                return None
            except redis.exceptions.AuthenticationError as e:
                # print(f"Authentication error for Redis at {self.host}:{self.port}: {e}", file=sys.stderr)
                return None

        def check_instance_liveness(self):
            """Checks if the Redis instance is alive (PING)."""
            client = self._get_redis_connection()
            if not client:
                return {"status": "CRITICAL", "message": f"Cannot connect to {self.host}:{self.port}"}
            try:
                if client.ping():
                    return {"status": "OK", "message": "Instance is alive (PONG)"}
            except Exception as e:
                return {"status": "CRITICAL", "message": f"PING failed: {e}"}
            return {"status": "CRITICAL", "message": "Instance is not responding to PING"}

        def get_instance_info(self, sections=None):
            """Retrieves INFO command output for specified sections."""
            client = self._get_redis_connection()
            if not client:
                return {"status": "CRITICAL", "message": f"Cannot connect to {self.host}:{self.port}"}
            info_data = {}
            try:
                if sections:
                    if isinstance(sections, str): sections = [sections]
                    for section in sections:
                        info_data[section] = client.info(section)
                else:
                    info_data['default'] = client.info()
                return {"status": "OK", "data": info_data}
            except Exception as e:
                return {"status": "CRITICAL", "message": f"Failed to get INFO: {e}", "data": {}}

        def check_replication_status(self):
            """Checks replication status (master/slave, lag)."""
            client = self._get_redis_connection()
            if not client:
                return {"status": "CRITICAL", "message": f"Cannot connect to {self.host}:{self.port}"}
            try:
                info = client.info('replication')
                role = info.get('role')
                replication_details = {"role": role}
                if role == 'master':
                    replication_details['connected_slaves'] = info.get('connected_slaves', 0)
                    slaves_info = []
                    for i in range(int(replication_details['connected_slaves'])):
                        slave_key = f'slave{i}'
                        if slave_key in info:
                             slaves_info.append(info[slave_key]) # format: ip=x,port=y,state=online,offset=z,lag=w
                    replication_details['slaves'] = slaves_info
                elif role == 'slave':
                    replication_details['master_host'] = info.get('master_host')
                    replication_details['master_port'] = info.get('master_port')
                    replication_details['master_link_status'] = info.get('master_link_status')
                    replication_details['master_last_io_seconds_ago'] = info.get('master_last_io_seconds_ago')
                    replication_details['master_sync_in_progress'] = info.get('master_sync_in_progress')
                    replication_details['slave_repl_offset'] = info.get('slave_repl_offset')
                    # master_offset might not be directly available, lag is more indicative
                    # slave_priority, slave_read_only
                return {"status": "OK", "data": replication_details}
            except Exception as e:
                return {"status": "CRITICAL", "message": f"Failed to get replication info: {e}", "data": {}}

    class SentinelHealthChecker:
        def __init__(self, sentinel_host, sentinel_port, master_name, sentinel_password=None):
            self.sentinel_host = sentinel_host
            self.sentinel_port = int(sentinel_port)
            self.master_name = master_name
            self.sentinel_password = sentinel_password # Note: redis-py Sentinel class handles auth slightly differently
            self.sentinel_client = None

        def _get_sentinel_connection(self):
            """Establishes and returns a Redis Sentinel connection."""
            # For Sentinel, it's better to use the redis.sentinel.Sentinel class
            # This simple check might not be robust enough for production Sentinel monitoring
            if self.sentinel_client:
                 try:
                    self.sentinel_client.ping()
                    return self.sentinel_client
                 except: #
                    self.sentinel_client = None

            try:
                # Basic client for direct sentinel commands if redis.sentinel.Sentinel is not preferred here.
                self.sentinel_client = redis.Redis(host=self.sentinel_host, port=self.sentinel_port,
                                                   password=self.sentinel_password, socket_connect_timeout=2,
                                                   socket_timeout=2, decode_responses=True)
                self.sentinel_client.ping()
                return self.sentinel_client
            except Exception as e:
                # print(f"Error connecting to Sentinel at {self.sentinel_host}:{self.sentinel_port}: {e}", file=sys.stderr)
                return None

        def check_sentinel_master_status(self):
            """Checks the status of the master monitored by Sentinel."""
            s = self._get_sentinel_connection()
            if not s:
                 return {"status": "CRITICAL", "message": f"Cannot connect to Sentinel {self.sentinel_host}:{self.sentinel_port}"}
            try:
                master_info = s.sentinel_master(self.master_name)
                # Example: master_info = {'name': 'mymaster', 'ip': '127.0.0.1', 'port': 6379, 'flags': 'master', ...}
                return {"status": "OK", "data": master_info}
            except redis.exceptions.ResponseError as e: # Master not found
                return {"status": "CRITICAL", "message": f"Sentinel master '{self.master_name}' not found or error: {e}", "data": {}}
            except Exception as e:
                return {"status": "CRITICAL", "message": f"Failed to get Sentinel master info for '{self.master_name}': {e}", "data": {}}


        def check_sentinel_slaves_status(self):
            """Checks the status of slaves for the monitored master."""
            s = self._get_sentinel_connection()
            if not s:
                 return {"status": "CRITICAL", "message": f"Cannot connect to Sentinel {self.sentinel_host}:{self.sentinel_port}"}
            try:
                slaves_info = s.sentinel_slaves(self.master_name)
                # Example: slaves_info = [{'name': 'x.x.x.x:6380', 'ip': 'x.x.x.x', 'port': 6380, ...}]
                return {"status": "OK", "data": slaves_info}
            except Exception as e:
                return {"status": "WARNING", "message": f"Failed to get Sentinel slaves info for '{self.master_name}': {e}", "data": []}


    def main():
        parser = argparse.ArgumentParser(description="Redis and Sentinel Health Checker.")
        # ... (argparse setup as per "Input Parameters" section) ...
        # For brevity, argument parsing is omitted here but should be implemented
        # Example:
        parser.add_argument("--host", default="localhost", help="Redis server host")
        parser.add_argument("--port", default=6379, type=int, help="Redis server port")
        parser.add_argument("--password", help="Redis server password")
        parser.add_argument("--sentinel-host", help="Sentinel host")
        parser.add_argument("--sentinel-port", default=26379, type=int, help="Sentinel port")
        parser.add_argument("--sentinel-master-name", help="Name of the master monitored by Sentinel")
        parser.add_argument("--sentinel-password", help="Sentinel password (for Sentinel server auth, not master auth)")
        parser.add_argument("--output-format", choices=['json', 'nagios'], default='json', help="Output format")
        parser.add_argument("--check-type", choices=['instance', 'replication', 'sentinel-master', 'sentinel-slaves', 'all-instance', 'all-sentinel'],
                            default='instance', help="Type of check to perform")


        args = parser.parse_args()
        results = {}

        if args.check_type in ['instance', 'replication', 'all-instance']:
            redis_checker = RedisHealthChecker(args.host, args.port, args.password)
            if args.check_type == 'instance' or args.check_type == 'all-instance':
                results['liveness'] = redis_checker.check_instance_liveness()
            if args.check_type == 'replication' or args.check_type == 'all-instance':
                results['replication'] = redis_checker.check_replication_status()
            if args.check_type == 'all-instance':
                 results['info_summary'] = redis_checker.get_instance_info(['server', 'clients', 'memory', 'persistence', 'stats', 'cpu'])


        if args.check_type in ['sentinel-master', 'sentinel-slaves', 'all-sentinel']:
            if not args.sentinel_host or not args.sentinel_master_name:
                print("Error: --sentinel-host and --sentinel-master-name are required for Sentinel checks.", file=sys.stderr)
                sys.exit(2)
            sentinel_checker = SentinelHealthChecker(args.sentinel_host, args.sentinel_port, args.sentinel_master_name, args.sentinel_password)
            if args.check_type == 'sentinel-master' or args.check_type == 'all-sentinel':
                results['sentinel_master_status'] = sentinel_checker.check_sentinel_master_status()
            if args.check_type == 'sentinel-slaves' or args.check_type == 'all-sentinel':
                 results['sentinel_slaves_status'] = sentinel_checker.check_sentinel_slaves_status()


        if args.output_format == 'json':
            print(json.dumps(results, indent=2))
        elif args.output_format == 'nagios':
            # Basic Nagios output: Determine overall status and print a summary
            # This part needs more sophisticated logic to aggregate status
            overall_status = "OK"
            messages = []
            critical_count = 0
            warning_count = 0

            for key, res_dict in results.items():
                if isinstance(res_dict, dict) and 'status' in res_dict :
                    messages.append(f"{key}: {res_dict.get('message', res_dict.get('status'))}")
                    if res_dict['status'] == 'CRITICAL':
                        overall_status = "CRITICAL"
                        critical_count += 1
                    elif res_dict['status'] == 'WARNING' and overall_status != "CRITICAL":
                        overall_status = "WARNING"
                        warning_count +=1
            
            if not results: # No checks run
                print("UNKNOWN: No checks performed.")
                sys.exit(3)

            summary_message = f"{overall_status} - Critical: {critical_count}, Warning: {warning_count}. Details: {'; '.join(messages)}"
            print(summary_message)
            if overall_status == "CRITICAL": sys.exit(2)
            if overall_status == "WARNING": sys.exit(1)
            sys.exit(0)

    if __name__ == "__main__":
        main()
    

## 6. Python Utility Modules Specification (`python_utils/`)

### 6.1 `python_utils/__init__.py`
*   **Purpose**: Standard Python package initializer. Makes the `python_utils` directory importable as a package.
*   **Logic**: Typically empty or may contain `__all__` definitions if specific submodule components are to be exported at the package level.
    python
    # python_utils/__init__.py
    # This file makes the python_utils directory a Python package.

    from .redis_connector import get_redis_connection
    from .session_utils import SessionAdminTools
    from .cache_admin_tools import CacheAdmin
    from .rate_limit_utils import RateLimitAdmin
    from .pubsub_diagnostics import PubSubAdmin

    __all__ = [
        "get_redis_connection",
        "SessionAdminTools",
        "CacheAdmin",
        "RateLimitAdmin",
        "PubSubAdmin",
    ]
    

### 6.2 `python_utils/redis_connector.py`
*   **Purpose**: Provides a centralized and reusable way to establish connections to Redis for other Python scripts within this repository.
*   **Class `RedisConnectionManager` (optional, if pooling or more complex logic is desired) or direct function**:
    python
    # python_utils/redis_connector.py
    import redis
    import os

    _connection_pool = None

    def get_redis_connection(host=None, port=None, password=None, db=0, use_pool=True, decode_responses=True):
        """
        Establishes and returns a Redis client instance.
        Uses environment variables as fallback if parameters are not provided.
        Manages a global connection pool if use_pool is True.
        """
        global _connection_pool

        resolved_host = host or os.getenv('REDIS_HOST', 'localhost')
        resolved_port = port or int(os.getenv('REDIS_PORT', 6379))
        resolved_password = password or os.getenv('REDIS_PASSWORD', None)
        resolved_db = db

        if use_pool:
            if _connection_pool is None or \
               _connection_pool.connection_kwargs.get('host') != resolved_host or \
               _connection_pool.connection_kwargs.get('port') != resolved_port or \
               _connection_pool.connection_kwargs.get('password') != resolved_password or \
               _connection_pool.connection_kwargs.get('db') != resolved_db:
                # Create or recreate pool if connection params changed or pool doesn't exist
                _connection_pool = redis.ConnectionPool(
                    host=resolved_host,
                    port=resolved_port,
                    password=resolved_password,
                    db=resolved_db,
                    decode_responses=decode_responses,
                    socket_connect_timeout=2, # seconds
                    socket_timeout=2 # seconds
                )
            return redis.Redis(connection_pool=_connection_pool)
        else:
            try:
                r = redis.Redis(
                    host=resolved_host,
                    port=resolved_port,
                    password=resolved_password,
                    db=resolved_db,
                    decode_responses=decode_responses,
                    socket_connect_timeout=2,
                    socket_timeout=2
                )
                r.ping() # Verify connection
                return r
            except redis.exceptions.ConnectionError as e:
                print(f"Error: Could not connect to Redis at {resolved_host}:{resolved_port}. {e}", file=sys.stderr)
                return None
            except redis.exceptions.AuthenticationError as e:
                print(f"Error: Authentication failed for Redis at {resolved_host}:{resolved_port}. {e}", file=sys.stderr)
                return None
    
*   **Logic**:
    *   The `get_redis_connection` function attempts to connect to Redis.
    *   It can optionally use a shared `redis.ConnectionPool` for efficiency if `use_pool` is `True`.
    *   Handles connection parameters (host, port, password, db).
    *   Includes basic error handling for connection failures.
    *   Uses environment variables (`REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`) as fallbacks.

### 6.3 `python_utils/session_utils.py`
*   **Purpose**: Provides administrative and diagnostic utilities for managing user sessions stored in Redis. Intended for use by system administrators, not by the main application's session handling logic.
*   **Class `SessionAdminTools`**:
    python
    # python_utils/session_utils.py
    from .redis_connector import get_redis_connection
    import json

    class SessionAdminTools:
        def __init__(self, redis_host=None, redis_port=None, redis_password=None, session_db_index=0):
            self.redis_client = get_redis_connection(
                host=redis_host,
                port=redis_port,
                password=redis_password,
                db=session_db_index,
                use_pool=False # For admin tools, direct connection might be simpler
            )
            if not self.redis_client:
                raise ConnectionError("Failed to connect to Redis for SessionAdminTools.")

        def count_active_sessions(self, session_key_prefix="session:"):
            """Counts active sessions by scanning keys with the given prefix."""
            count = 0
            # SCAN is preferred over KEYS for production environments
            for _ in self.redis_client.scan_iter(match=f"{session_key_prefix}*"):
                count += 1
            return count

        def get_session_details(self, session_id_full_key):
            """Retrieves and potentially decodes session data for a given full session key."""
            # Assuming session_id_full_key is like "session:uuid"
            try:
                session_data_raw = self.redis_client.get(session_id_full_key)
                if session_data_raw:
                    # Attempt to decode if it's JSON, otherwise return raw
                    try:
                        return json.loads(session_data_raw)
                    except json.JSONDecodeError:
                        return session_data_raw # Or handle as plain string/bytes
                return None
            except Exception as e:
                print(f"Error getting session details for {session_id_full_key}: {e}")
                return None

        def list_sessions_by_pattern(self, pattern="session:*", count=100):
            """Lists session keys matching a pattern (use SCAN for safety)."""
            sessions = []
            cursor = '0'
            while cursor != 0:
                cursor, keys = self.redis_client.scan(cursor=cursor, match=pattern, count=count)
                sessions.extend(keys)
                if len(sessions) >= count and count > 0 : # limit results if count is specified
                    break
            return sessions


        def clear_session(self, session_id_full_key):
            """Clears/deletes a specific session by its full key."""
            try:
                deleted_count = self.redis_client.delete(session_id_full_key)
                return deleted_count > 0
            except Exception as e:
                print(f"Error clearing session {session_id_full_key}: {e}")
                return False

    # Example usage (if run directly for testing)
    if __name__ == '__main__':
        # Assumes Redis is running locally on default port for this example
        try:
            admin_tools = SessionAdminTools()
            print(f"Active sessions: {admin_tools.count_active_sessions()}")
            
            # Example: list some sessions
            some_sessions = admin_tools.list_sessions_by_pattern(count=5)
            print(f"Some session keys: {some_sessions}")

            # If you have a known session key, e.g., "session:test-user-123"
            # (you'd need to set one up for this to work)
            # test_session_key = "session:test-user-123"
            # self.redis_client.set(test_session_key, json.dumps({"user_id": "123", "role": "admin"}))
            # print(f"Details for {test_session_key}: {admin_tools.get_session_details(test_session_key)}")
            # print(f"Clearing {test_session_key}: {admin_tools.clear_session(test_session_key)}")

        except ConnectionError as e:
            print(e)
    
*   **Relation to Requirements**: `SEC-002` (Session Management). This tool helps in auditing and managing the session data.

### 6.4 `python_utils/cache_admin_tools.py`
*   **Purpose**: Provides administrative utilities for managing general-purpose caches (e.g., templates, user preferences) stored in Redis.
*   **Class `CacheAdmin`**:
    python
    # python_utils/cache_admin_tools.py
    from .redis_connector import get_redis_connection

    class CacheAdmin:
        def __init__(self, redis_host=None, redis_port=None, redis_password=None, cache_db_index=1):
            self.redis_client = get_redis_connection(
                host=redis_host,
                port=redis_port,
                password=redis_password,
                db=cache_db_index,
                use_pool=False
            )
            if not self.redis_client:
                raise ConnectionError("Failed to connect to Redis for CacheAdmin.")

        def list_cache_keys(self, pattern="cache:*", count=1000):
            """Lists cache keys matching a pattern using SCAN."""
            keys_found = []
            cursor = '0'
            while cursor != 0:
                cursor, keys = self.redis_client.scan(cursor=cursor, match=pattern, count=count)
                keys_found.extend(keys)
                if len(keys_found) >= count and count > 0: # for practical limits
                    break
            return keys_found

        def get_cache_value(self, key):
            """Retrieves the value of a cache key."""
            # Value might be serialized (e.g., JSON, Pickle). This retrieves raw.
            try:
                return self.redis_client.get(key)
            except Exception as e:
                print(f"Error getting cache value for {key}: {e}")
                return None

        def get_cache_ttl(self, key):
            """Gets the Time To Live (TTL) for a cache key in seconds."""
            try:
                ttl = self.redis_client.ttl(key)
                return ttl # -2 if key does not exist, -1 if no TTL
            except Exception as e:
                print(f"Error getting TTL for {key}: {e}")
                return None


        def delete_cache_key(self, key):
            """Deletes a specific cache key."""
            try:
                deleted_count = self.redis_client.delete(key)
                return deleted_count > 0
            except Exception as e:
                print(f"Error deleting cache key {key}: {e}")
                return False

        def flush_cache_by_pattern(self, pattern="cache:*"):
            """Deletes all keys matching a pattern. Use with extreme caution in production."""
            # WARNING: This can be slow and blocking depending on the number of keys.
            # Prefer targeted deletion or Redis eviction policies.
            keys_to_delete = self.list_cache_keys(pattern, count=0) # count=0 to get all
            deleted_count = 0
            if keys_to_delete:
                # Consider batching deletes for very large numbers of keys
                deleted_count = self.redis_client.delete(*keys_to_delete)
            return deleted_count
    
*   **Relation to Requirements**: `Section 5.2.2` (Caching component).

### 6.5 `python_utils/rate_limit_utils.py`
*   **Purpose**: Offers administrative utilities for inspecting and managing rate limit counters in Redis.
*   **Class `RateLimitAdmin`**:
    python
    # python_utils/rate_limit_utils.py
    from .redis_connector import get_redis_connection

    class RateLimitAdmin:
        def __init__(self, redis_host=None, redis_port=None, redis_password=None, rate_limit_db_index=3):
            self.redis_client = get_redis_connection(
                host=redis_host,
                port=redis_port,
                password=redis_password,
                db=rate_limit_db_index,
                use_pool=False
            )
            if not self.redis_client:
                raise ConnectionError("Failed to connect to Redis for RateLimitAdmin.")

        def get_rate_limit_value(self, counter_key):
            """Gets the current value of a rate limit counter."""
            try:
                value = self.redis_client.get(counter_key)
                return int(value) if value is not None else None
            except Exception as e:
                print(f"Error getting rate limit value for {counter_key}: {e}")
                return None

        def reset_rate_limit_counter(self, counter_key):
            """Resets a specific rate limit counter (deletes the key)."""
            try:
                deleted_count = self.redis_client.delete(counter_key)
                return deleted_count > 0
            except Exception as e:
                print(f"Error resetting rate limit counter {counter_key}: {e}")
                return False

        def list_rate_limit_keys(self, pattern="ratelimit:*", count=1000):
            """Lists rate limit keys matching a pattern using SCAN."""
            keys_found = []
            cursor = '0'
            while cursor != 0:
                cursor, keys = self.redis_client.scan(cursor=cursor, match=pattern, count=count)
                keys_found.extend(keys)
                if len(keys_found) >= count and count > 0:
                    break
            return keys_found
    
*   **Relation to Requirements**: `Section 5.2.2` (Rate limiting counters functionality).

### 6.6 `python_utils/pubsub_diagnostics.py`
*   **Purpose**: Provides diagnostic tools for administrators to monitor Redis Pub/Sub channels.
*   **Class `PubSubAdmin`**:
    python
    # python_utils/pubsub_diagnostics.py
    from .redis_connector import get_redis_connection

    class PubSubAdmin:
        def __init__(self, redis_host=None, redis_port=None, redis_password=None, pubsub_db_index=2):
            # Note: PUBSUB commands are not affected by SELECT db, they are global.
            # However, connector might need a DB for other operations or consistency.
            self.redis_client = get_redis_connection(
                host=redis_host,
                port=redis_port,
                password=redis_password,
                db=pubsub_db_index, # Or default DB if PUBSUB is global only
                use_pool=False
            )
            if not self.redis_client:
                raise ConnectionError("Failed to connect to Redis for PubSubAdmin.")

        def list_active_channels(self, pattern="*"):
            """Lists active Pub/Sub channels matching a pattern."""
            try:
                return self.redis_client.pubsub_channels(pattern=pattern)
            except Exception as e:
                print(f"Error listing active channels with pattern {pattern}: {e}")
                return []

        def get_channel_subscriber_count(self, channel_name):
            """Gets the number of subscribers for a specific channel."""
            try:
                # PUBSUB NUMSUB returns a list of [channel, count, channel2, count2, ...]
                result = self.redis_client.pubsub_numsub(channel_name)
                if result and len(result) == 2:
                    return result[1] # The count for the requested channel
                return 0
            except Exception as e:
                print(f"Error getting subscriber count for channel {channel_name}: {e}")
                return None


        def publish_test_message(self, channel_name, message="Test message"):
            """Publishes a test message to a specified channel."""
            try:
                # Returns the number of clients that received the message
                return self.redis_client.publish(channel_name, message)
            except Exception as e:
                print(f"Error publishing test message to channel {channel_name}: {e}")
                return None
    
*   **Relation to Requirements**: `Section 5.2.2` (Pub/Sub mechanism for Notification Service).

## 7. Environment Configuration
The following environment variables should be configurable by Ansible when deploying Redis and Sentinel instances, based on the templates:

**For `redis.conf.tpl`:**
*   `REDIS_PORT`: Port for the Redis server (e.g., 6379, 6380 for replicas).
*   `REDIS_BIND_IP`: IP address to bind to.
*   `REDIS_PROTECTED_MODE`: `yes` or `no`.
*   `REDIS_DAEMONIZE`: `yes` or `no`.
*   `REDIS_DATABASES`: Number of databases.
*   `REDIS_RDB_COMPRESSION`: `yes` or `no`.
*   `REDIS_AOF_ENABLED`: `yes` or `no`.
*   `REDIS_AOF_FSYNC_POLICY`: `everysec`, `always`, `no`.
*   `REDIS_PASSWORD`: The password for Redis server access (from KMS/Vault).
*   `REDIS_MAX_CLIENTS`: Maximum number of client connections.
*   `REDIS_MAX_MEMORY`: Maximum memory Redis can use (e.g., `2gb`).
*   `REDIS_MAXMEMORY_POLICY`: Eviction policy.
*   `REDIS_KEYSPACE_EVENTS`: Keyspace notification events string.

**For `sentinel.conf.tpl`:**
*   `SENTINEL_PORT`: Port for the Sentinel instance.
*   `SENTINEL_DAEMONIZE`: `yes` or `no`.
*   `SENTINEL_MASTER_NAME`: Name of the master Redis instance being monitored.
*   `SENTINEL_MASTER_IP`: IP address of the master Redis instance.
*   `SENTINEL_MASTER_PORT`: Port of the master Redis instance.
*   `SENTINEL_QUORUM`: Number of Sentinels needed to agree on a failover.
*   `SENTINEL_DOWN_AFTER_MS`: Time in ms for a master to be considered down.
*   `SENTINEL_PARALLEL_SYNCS`: Number of replicas that can be reconfigured to follow the new master at the same time.
*   `SENTINEL_FAILOVER_TIMEOUT`: Timeout for failover operations.
*   `SENTINEL_MASTER_PASSWORD`: Password for the master Redis instance (from KMS/Vault).
*   `SENTINEL_PASSWORD`: (Optional) Password for the Sentinel instance itself (from KMS/Vault).
*   `SENTINEL_USER`: (Optional) User for Sentinel ACLs if password is set.

## 8. Deployment and Management
*   Deployment of Redis servers and Sentinel instances will be managed by Ansible, utilizing the `.tpl` configuration files.
*   Ansible playbooks will be responsible for:
    *   Installing Redis.
    *   Copying and rendering the configuration templates with environment-specific values (including injecting secrets from a vault).
    *   Setting up directories and permissions.
    *   Managing the Redis and Sentinel services (start, stop, enable on boot) using the `manage_redis_server.sh` and `manage_sentinel.sh` scripts or directly via systemd/init.d.
*   The operational scripts (`manage_*.sh`) provide manual control and status checking capabilities if needed outside of Ansible.

## 9. Security Considerations (Summary)
*   **Authentication**: `requirepass` for Redis servers and Sentinels.
*   **Authorization**: (If using Redis ACLs with Sentinel, though simpler password auth is common).
*   **Network Security**: `bind` to specific IPs, `protected-mode`. Firewalls at OS/network level.
*   **Data Encryption**: While Redis itself doesn't encrypt data at rest on disk natively (unless through filesystem encryption), sensitive data passed to Redis (e.g., session content if it contains PII before serialization) should be handled carefully by applications. This repository focuses on Redis operational security.
*   **Regular Updates**: OS and Redis software patched regularly via Ansible.

## 10. Monitoring and Health Checks
*   The `scripts/monitoring/check_redis_health.py` script is the primary tool for detailed health checks.
*   Key metrics to monitor via Prometheus (using a Redis exporter and data from `check_redis_health.py` output):
    *   `uptime_in_seconds`
    *   `connected_clients`
    *   `used_memory`, `used_memory_rss`, `mem_fragmentation_ratio`
    *   `instantaneous_ops_per_sec`
    *   `total_commands_processed`
    *   `keyspace_hits`, `keyspace_misses` (cache hit rate)
    *   `evicted_keys`
    *   `role` (master/slave)
    *   For slaves: `master_link_status`, `master_last_io_seconds_ago`, `slave_repl_offset`, `master_sync_in_progress`.
    *   For Sentinel: `sentinel_masters`, `sentinel_slaves_count`, `sentinel_master_status` (flags), `sentinel_tilt` (if in tilt mode).
*   Alerts should be configured in Prometheus/Alertmanager for:
    *   Instance down (PING fails).
    *   High memory usage (approaching `maxmemory`).
    *   Low cache hit rate.
    *   Replication issues (link down, high lag).
    *   Sentinel unable to reach master or quorum lost.
    *   Sentinel failover events.

## 11. Backup and Persistence (Summary)
*   Persistence configured via `redis.conf.tpl` (RDB snapshots and/or AOF).
*   Backup of RDB files and AOF files (if used) should be handled by standard server backup procedures (e.g., backing up `/var/lib/redis/`).
*   For DR, if Redis data needs to be recovered, restoring these files to a new instance is the primary method. Sentinel helps in HA but doesn't replace backups for disaster recovery of data.

This SDS outlines the design for configuring and managing Redis, ensuring it meets the performance, availability, and security needs of the CreativeFlow AI platform.