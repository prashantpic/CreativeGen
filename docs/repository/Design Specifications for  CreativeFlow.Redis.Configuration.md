# Software Design Specification: CreativeFlow.Redis.Configuration

## 1. Introduction

### 1.1. Purpose
This document details the design specifications for the `CreativeFlow.Redis.Configuration` repository. This repository is responsible for providing configuration templates, setup scripts, operational utilities, and Ansible integration components for deploying and managing Redis instances within the CreativeFlow AI platform. Redis serves critical roles including session management, content caching, rate limiting, and as a Pub/Sub mechanism for the Notification Service.

### 1.2. Scope
The scope of this repository includes:
*   Base configuration templates for Redis server (`redis.conf`) and Redis Sentinel (`sentinel.conf`).
*   Shell scripts for:
    *   Dynamically generating configuration files from templates.
    *   Setting up standalone Redis instances.
    *   Setting up Redis Sentinel high-availability topologies.
    *   Setting up Redis Cluster nodes and forming a cluster.
    *   Managing Redis/Sentinel services (start, stop, status).
    *   Executing arbitrary Redis commands.
*   Lua scripts for atomic Redis operations, specifically for session management and rate limiting.
*   Ansible integration artifacts, including variable files and Jinja2 templates for automated Redis and Sentinel configuration management.

### 1.3. Definitions, Acronyms, and Abbreviations
*   **Redis**: Remote Dictionary Server, an in-memory data structure store.
*   **Sentinel**: Redis high availability solution.
*   **Cluster**: Redis distributed sharding solution.
*   **RDB**: Redis Database Backup (snapshotting).
*   **AOF**: Append Only File (persistence).
*   **TTL**: Time To Live.
*   **Pub/Sub**: Publish/Subscribe messaging paradigm.
*   **HA**: High Availability.
*   **IaC**: Infrastructure as Code.
*   **J2**: Jinja2 templating engine.
*   **SDS**: Software Design Specification.
*   **CI/CD**: Continuous Integration / Continuous Deployment.
*   **SEC-002**: Requirement for session management using Redis.
*   **DEP-001**: Requirement detailing Redis server specifications.

## 2. System Overview
The `CreativeFlow.Redis.Configuration` repository provides the foundational elements for deploying and managing Redis, a key data caching and messaging component within the CreativeFlow AI platform. It supports different Redis deployment topologies (standalone, Sentinel HA, Cluster) to meet varying needs for performance, scalability, and availability as outlined in system architecture (Section 5.1) and server specifications (DEP-001). The configurations and scripts ensure Redis is optimized for its roles in session management (SEC-002), general caching, Pub/Sub, and rate limiting (Section 5.2.2).

## 3. Design Considerations

### 3.1. Assumptions and Dependencies
*   Target Linux servers will have Bash shell and standard Unix utilities (`sed`, `awk`, `grep`) available for script execution.
*   `redis-cli` and `redis-server` (or `redis-sentinel`) executables are expected to be in the system PATH or at a known location for operational scripts.
*   Ansible is used as the primary configuration management tool for production deployments, leveraging the Jinja2 templates and variables provided.
*   Secure secret management (e.g., HashiCorp Vault or Ansible Vault) is used for Redis passwords.

### 3.2. General Design Principles
*   **Modularity**: Scripts and templates are designed to be modular and reusable.
*   **Parameterization**: Configurations are generated from templates with dynamic parameter substitution to support various environments and instance types.
*   **Automation**: Emphasis on automating setup and configuration tasks to ensure consistency and reduce manual error.
*   **Security**: Default configurations and scripts promote secure Redis deployments (e.g., password protection, non-default ports where appropriate).
*   **Idempotency**: Setup scripts and Ansible playbooks (leveraging these artifacts) should aim for idempotency.

## 4. Component Design

### 4.1. Configuration Templates

#### 4.1.1. `config/redis.conf.template`
*   **Description**: Base Redis server configuration template.
*   **Purpose**: To serve as a standardized and customizable foundation for configuring Redis server instances.
*   **Key Directives and Sections**:
    *   **Networking**:
        *   `bind ##REDIS_BIND_IP##` (Placeholder for bind IP, e.g., 0.0.0.0 or specific interface)
        *   `port ##REDIS_PORT##` (Placeholder for Redis port)
        *   `protected-mode yes` (Default, can be overridden if binding to specific IPs)
        *   `tcp-keepalive 300`
    *   **Security**:
        *   `requirepass "##REDIS_PASSWORD##"` (Placeholder for password)
        *   Consider `rename-command CONFIG ""` or similar for hardening.
    *   **General**:
        *   `daemonize yes` (For background operation if not managed by systemd)
        *   `pidfile /var/run/redis_##REDIS_PORT##.pid`
        *   `loglevel notice`
        *   `logfile "/var/log/redis/redis_##REDIS_PORT##.log"`
        *   `databases 16` (Default, can be adjusted)
    *   **Persistence (RDB)**:
        *   `save 900 1`
        *   `save 300 10`
        *   `save 60 10000`
        *   `stop-writes-on-bgsave-error yes`
        *   `rdbcompression yes`
        *   `rdbchecksum yes`
        *   `dbfilename dump_##REDIS_PORT##.rdb`
        *   `dir /var/lib/redis/##REDIS_PORT##`
    *   **Persistence (AOF)**:
        *   `appendonly ##AOF_ENABLED##` (Placeholder: `yes` or `no`)
        *   `appendfilename "appendonly_##REDIS_PORT##.aof"`
        *   `appendfsync everysec` (Default, can be `always` or `no` based on durability needs)
        *   `no-appendfsync-on-rewrite no`
        *   `auto-aof-rewrite-percentage 100`
        *   `auto-aof-rewrite-min-size 64mb`
    *   **Memory Management (Critical for SEC-002, Section 5.2.2, DEP-001)**:
        *   `maxmemory ##MAXMEMORY_MB##mb` (Placeholder for max memory in MB)
        *   `maxmemory-policy allkeys-lru` (Recommended for general caching and sessions. Can be `volatile-lru` or other policies based on specific use case. `allkeys-lru` evicts any key using an LRU algorithm when `maxmemory` is reached.)
    *   **Lua Scripting**:
        *   `lua-time-limit 5000`
    *   **Slow Log**:
        *   `slowlog-log-slower-than 10000`
        *   `slowlog-max-len 128`
    *   **Keyspace Notifications (for Pub/Sub, Section 5.2.2)**:
        *   `notify-keyspace-events KEA` (Example: All keyspace events for all event types. Can be more specific, e.g., `Ex` for expired keys if used for session cleanup by a separate process).
    *   **Client Limits**:
        *   `maxclients 10000`
    *   **Cluster Mode (Conditional)**:
        *   `##IF_CLUSTER_MODE##cluster-enabled yes`
        *   `##IF_CLUSTER_MODE##cluster-config-file nodes-##REDIS_PORT##.conf`
        *   `##IF_CLUSTER_MODE##cluster-node-timeout 15000`
        *   `##IF_CLUSTER_MODE##cluster-announce-ip ##ANNOUNCE_IP##`
        *   `##IF_CLUSTER_MODE##cluster-announce-port ##REDIS_PORT##`
        *   `##IF_CLUSTER_MODE##cluster-announce-bus-port ##CLUSTER_BUS_PORT##`
    *   **Replication (for Slaves)**:
        *   `##IF_SLAVE_MODE##replicaof ##MASTER_IP## ##MASTER_PORT##`
        *   `##IF_SLAVE_MODE##masterauth "##MASTER_PASSWORD##"`
        *   `replica-serve-stale-data yes`
*   **Placeholders**: `##REDIS_BIND_IP##`, `##REDIS_PORT##`, `##REDIS_PASSWORD##`, `##AOF_ENABLED##`, `##MAXMEMORY_MB##`, `##IF_CLUSTER_MODE##`, `##ANNOUNCE_IP##`, `##CLUSTER_BUS_PORT##`, `##IF_SLAVE_MODE##`, `##MASTER_IP##`, `##MASTER_PORT##`, `##MASTER_PASSWORD##`.

#### 4.1.2. `config/sentinel.conf.template`
*   **Description**: Base Redis Sentinel configuration template.
*   **Purpose**: To provide a standardized template for configuring Redis Sentinel instances for HA.
*   **Key Directives**:
    *   `port ##SENTINEL_PORT##`
    *   `daemonize yes`
    *   `pidfile /var/run/redis-sentinel_##SENTINEL_PORT##.pid`
    *   `logfile "/var/log/redis/sentinel_##SENTINEL_PORT##.log"`
    *   `dir "/tmp"` (or a persistent directory)
    *   `sentinel monitor ##MASTER_NAME## ##MASTER_IP## ##MASTER_PORT## ##QUORUM##`
    *   `sentinel down-after-milliseconds ##MASTER_NAME## ##DOWN_AFTER_MS##`
    *   `sentinel parallel-syncs ##MASTER_NAME## 1`
    *   `sentinel failover-timeout ##MASTER_NAME## ##FAILOVER_TIMEOUT_MS##`
    *   `sentinel auth-pass ##MASTER_NAME## "##MASTER_PASSWORD##"` (If master has password)
    *   `sentinel announce-ip ##ANNOUNCE_IP##` (Optional, for NAT/Docker environments)
    *   `sentinel announce-port ##SENTINEL_PORT##` (Optional)
*   **Placeholders**: `##SENTINEL_PORT##`, `##MASTER_NAME##`, `##MASTER_IP##`, `##MASTER_PORT##`, `##QUORUM##`, `##DOWN_AFTER_MS##`, `##FAILOVER_TIMEOUT_MS##`, `##MASTER_PASSWORD##`, `##ANNOUNCE_IP##`.

### 4.2. Shell Scripts

#### 4.2.1. `scripts/common/utils.sh`
*   **Description**: Common utility functions.
*   **Purpose**: Centralize shared shell script logic.
*   **Functions**:
    *   `log_info(message)`: Echoes `[INFO] <timestamp>: message`.
    *   `log_error(message)`: Echoes `[ERROR] <timestamp>: message` to stderr.
    *   `verify_command(command_name)`: Checks if `command_name` exists in PATH using `command -v`. Returns 0 if found, 1 otherwise.
    *   `is_valid_ip(ip_address)`: Validates IP address format (IPv4) using regex. Returns 0 for valid, 1 for invalid.
    *   `is_valid_port(port_number)`: Checks if port number is within 1-65535. Returns 0 for valid, 1 for invalid.

#### 4.2.2. `scripts/setup/apply_config.sh`
*   **Description**: Applies configuration from a template.
*   **Purpose**: Dynamically generate Redis/Sentinel config files.
*   **Usage**: `./apply_config.sh <template_file> <output_file> "KEY1=VALUE1" "KEY2=VALUE2" ...`
*   **Logic**:
    1.  Sources `scripts/common/utils.sh`.
    2.  Validates arguments (template exists, output path writable).
    3.  Copies template to output file.
    4.  Iterates through `KEY=VALUE` pairs. For each pair:
        *   Extracts KEY and VALUE.
        *   Uses `sed -i "s|##${KEY}##|${VALUE}|g" "${output_file}"` to replace placeholders. Special characters in VALUE might need escaping or a different `sed` delimiter.
    5.  Logs success or errors.

#### 4.2.3. `scripts/setup/setup_redis_standalone.sh`
*   **Description**: Sets up a standalone Redis instance.
*   **Purpose**: Automate single Redis server configuration.
*   **Usage**: `./setup_redis_standalone.sh --port <port> --password <pass> --maxmemory <MB> --aof <yes|no> [--bind-ip <ip>] [--config-dir /etc/redis] [--data-dir /var/lib/redis] [--log-dir /var/log/redis]`
*   **Logic**:
    1.  Sources `scripts/common/utils.sh`.
    2.  Parses command-line arguments (using `getopt` or simple loop).
    3.  Defines default values if arguments are not provided.
    4.  Validates inputs (port, IP, maxmemory format).
    5.  Creates `config-dir`, `data-dir`, `log-dir` if they don't exist, setting appropriate permissions (e.g., for `redis` user).
    6.  Constructs key-value pairs for `apply_config.sh`:
        *   `REDIS_PORT=$port`
        *   `REDIS_PASSWORD=$password`
        *   `MAXMEMORY_MB=$maxmemory`
        *   `AOF_ENABLED=$aof`
        *   `REDIS_BIND_IP=$bind_ip` (or 0.0.0.0 if not specified)
        *   Other relevant placeholders from `redis.conf.template`.
    7.  Calls `./apply_config.sh "${template_dir}/redis.conf.template" "${config_dir}/redis_${port}.conf" <key_value_pairs>`.
    8.  Outputs path to generated config and instructions to start if not automated.
    9.  (Optional) Calls `./scripts/operational/manage_service.sh start redis "${config_dir}/redis_${port}.conf"` if direct process management is intended.

#### 4.2.4. `scripts/setup/setup_redis_sentinel_topology.sh`
*   **Description**: Configures Redis master, slave(s), and Sentinels.
*   **Purpose**: Automate Redis HA Sentinel deployment.
*   **Usage**: `./setup_redis_sentinel_topology.sh --master-ip <ip> --master-port <port> --master-pass <pass> --slave-nodes "ip1:port1 ip2:port2" --sentinel-nodes "ipA:portA ipB:portB ipC:portC" --sentinel-quorum <N> [--config-base-dir /etc/redis] ...`
*   **Logic**:
    1.  Sources `utils.sh`. Parses arguments.
    2.  **Master Setup**:
        *   Generates `redis_master_${master_port}.conf` using `apply_config.sh` and `redis.conf.template`. Key settings: port, password, persistence. No `replicaof`.
    3.  **Slave Setup (for each slave node)**:
        *   Generates `redis_slave_${slave_port}.conf`. Key settings: port, password, `replicaof ${master_ip} ${master_port}`, `masterauth ${master_pass}`.
    4.  **Sentinel Setup (for each sentinel node)**:
        *   Generates `sentinel_${sentinel_port}.conf` using `apply_config.sh` and `sentinel.conf.template`.
        *   Placeholders: `SENTINEL_PORT`, `MASTER_NAME` (e.g., "mymaster"), `MASTER_IP`, `MASTER_PORT`, `QUORUM`, `DOWN_AFTER_MS` (e.g., 30000), `FAILOVER_TIMEOUT_MS` (e.g., 180000), `MASTER_PASSWORD`.
    5.  Provides instructions or attempts to start Redis master, then slaves, then Sentinels.

#### 4.2.5. `scripts/setup/setup_redis_cluster_nodes.sh`
*   **Description**: Configures nodes for Redis Cluster and forms the cluster.
*   **Purpose**: Automate Redis Cluster creation.
*   **Usage**: `./setup_redis_cluster_nodes.sh --nodes "ip1:port1 ip2:port2 ip3:port3 ip4:port4 ip5:port5 ip6:port6" --replicas <N> [--password <pass>] [--config-base-dir /etc/redis/cluster]`
*   **Logic**:
    1.  Sources `utils.sh`. Parses arguments.
    2.  **Node Configuration (for each node in `--nodes`)**:
        *   Extract IP and Port.
        *   Generates `redis_cluster_node_${port}.conf` using `apply_config.sh` and `redis.conf.template`.
        *   Key `redis.conf.template` placeholders substituted: `REDIS_PORT`, `REDIS_PASSWORD`, `IF_CLUSTER_MODEcluster-enabled yes`, `IF_CLUSTER_MODEcluster-config-file nodes-${port}.conf`, `IF_CLUSTER_MODEcluster-node-timeout 15000`, etc.
        *   Creates data directory for each node.
    3.  Starts all configured Redis instances.
    4.  Waits for nodes to be up (e.g., using `redis-cli PING` in a loop).
    5.  Constructs the `redis-cli --cluster create <node_list> --cluster-replicas <replicas>` command. If password is set, may need to handle authentication for `redis-cli` or ensure nodes are configured with `masteruser` and `masterauth` for cluster operations if cluster auth is enabled.
    6.  Executes the `redis-cli --cluster create` command.

#### 4.2.6. `scripts/operational/manage_service.sh`
*   **Description**: Manages Redis/Sentinel services.
*   **Purpose**: Consistent interface for service lifecycle.
*   **Usage**: `./manage_service.sh <start|stop|restart|status> <redis|sentinel> <config_file_path_or_service_name_if_systemd>`
*   **Logic**:
    1.  Sources `utils.sh`. Parses arguments.
    2.  Detects if `systemctl` is available.
    3.  **If systemd**:
        *   Uses `systemctl $action $service_type@$service_identifier` (e.g., `redis-server@myconfig` if service units are named like that) or `systemctl $action $service_identifier` (e.g. `redis` or `redis-sentinel`).
    4.  **If not systemd (direct process management)**:
        *   `start`: `redis-server $config_file_path` or `redis-sentinel $config_file_path`.
        *   `stop`: `redis-cli -p <port_from_config> [-a <password_from_config>] shutdown` or `kill $(cat <pidfile_from_config>)`.
        *   `status`: Check if process is running via PID file or `pgrep`.
        *   `restart`: `stop` then `start`.
    5.  Requires parsing port/password/pidfile from config if managing directly.

#### 4.2.7. `scripts/operational/redis_command_executor.sh`
*   **Description**: Wrapper for `redis-cli`.
*   **Purpose**: Securely execute Redis commands.
*   **Usage**: `./redis_command_executor.sh --host <host> --port <port> [--password <pass>] --command "COMMAND [ARGS...]"`
*   **Logic**:
    1.  Sources `utils.sh`. Parses arguments.
    2.  Constructs `redis-cli_command="redis-cli"`.
    3.  Appends `-h $host -p $port`.
    4.  If password provided, appends `-a "$password"`.
    5.  Appends the command string: `$redis_cli_command $command_to_execute`.
    6.  Executes the command using `eval` or directly if command string is safe.
    7.  Outputs result or error.

### 4.3. Lua Scripts

#### 4.3.1. `scripts/lua/session_operations.lua`
*   **Description**: Atomic session operations (SEC-002).
*   **Purpose**: Ensure atomicity for session updates and TTL extensions.
*   **Key Functions (Conceptual, to be embedded in Lua script string for EVAL)**:
    *   **`updateAndExtendSession(KEYS[1], ARGV[1], ARGV[2], ARGV[3])`**
        *   `KEYS[1]`: Session key (e.g., `session:user123`)
        *   `ARGV[1]`: Field to update (or use HMSET with multiple field/value pairs in ARGV)
        *   `ARGV[2]`: New value for the field
        *   `ARGV[3]`: New TTL in seconds
        *   **Logic**:
            lua
            -- Example for HSET, could also be SET if session data is a single string
            redis.call('HSET', KEYS[1], ARGV[1], ARGV[2])
            redis.call('EXPIRE', KEYS[1], ARGV[3])
            return 1 -- or some status
            
    *   **`getAndExtendSession(KEYS[1], ARGV[1])`**
        *   `KEYS[1]`: Session key
        *   `ARGV[1]`: New TTL in seconds
        *   **Logic**:
            lua
            local session_data = redis.call('HGETALL', KEYS[1]) -- or GET
            if #session_data > 0 then
                redis.call('EXPIRE', KEYS[1], ARGV[1])
            end
            return session_data
            
*   **Usage**: Loaded and called via `EVALSHA` or `EVAL` by application services needing session management.

#### 4.3.2. `scripts/lua/rate_limiter_flexible.lua`
*   **Description**: Flexible rate limiter.
*   **Purpose**: Efficient, server-side rate limiting.
*   **Key Functions (Conceptual for Sliding Window)**:
    *   **`isAllowedSlidingWindow(KEYS[1], ARGV[1], ARGV[2], ARGV[3])`**
        *   `KEYS[1]`: Rate limit key (e.g., `ratelimit:user123:api_endpoint`)
        *   `ARGV[1]`: Current timestamp (seconds or milliseconds)
        *   `ARGV[2]`: Window size in seconds
        *   `ARGV[3]`: Maximum requests in window
        *   **Logic**:
            lua
            local key = KEYS[1]
            local now = tonumber(ARGV[1])
            local window = tonumber(ARGV[2])
            local limit = tonumber(ARGV[3])
            local clear_before = now - window

            -- Remove old entries
            redis.call('ZREMRANGEBYSCORE', key, 0, clear_before)

            -- Get current count
            local count = redis.call('ZCARD', key)

            if count < limit then
                -- Add current request
                redis.call('ZADD', key, now, now)
                -- Set TTL on the key to clean up if no activity
                redis.call('EXPIRE', key, window)
                return 0 -- Allowed
            else
                return 1 -- Denied
            end
            
*   **Usage**: Called via `EVALSHA` or `EVAL` by API Gateway or services needing rate limiting.

### 4.4. Ansible Integration

#### 4.4.1. `ansible_integration/vars/redis_config_variables.yml`
*   **Description**: Centralized Ansible variables for Redis configurations.
*   **Purpose**: Provide structured, environment-specific parameters for Ansible.
*   **Structure**:
    yaml
    # Defaults (can be overridden by environment or host vars)
    redis_default_port: 6379
    redis_default_bind_ip: "127.0.0.1" # Secure default
    redis_default_maxmemory_factor: 0.5 # e.g., 50% of total system RAM
    redis_default_aof_enabled: "yes"
    redis_default_loglevel: "notice"
    redis_user: "redis"
    redis_group: "redis"
    redis_config_dir: "/etc/redis"
    redis_data_dir_base: "/var/lib/redis"
    redis_log_dir: "/var/log/redis"

    sentinel_default_port: 26379
    sentinel_default_quorum: 2
    sentinel_default_down_after_ms: 30000
    sentinel_default_failover_timeout_ms: 180000

    # Example for a specific role or group of servers
    # These could be in group_vars/redis_masters.yml, host_vars/server1.yml etc.
    # redis_instances:
    #   - port: 6379
    #     role: master # or standalone, slave, cluster_node
    #     password_vault_var: "redis_master_6379_password"
    #     maxmemory_mb: 1024 # Overrides calculation from factor
    #     aof_enabled: "yes"
    #     # For slaves:
    #     # master_ip: "x.x.x.x"
    #     # master_port: 6379
    #     # master_password_vault_var: "redis_master_6379_password"
    #     # For cluster:
    #     # cluster_enabled: "yes"
    #     # announce_ip: "public_ip_of_node"
    #     # cluster_bus_port: 16379 # port + 10000

    # sentinel_configs:
    #   - port: 26379
    #     monitors:
    #       - name: "mymaster"
    #         ip: "x.x.x.x" # Master IP
    #         port: 6379   # Master Port
    #         quorum: 2
    #         auth_pass_vault_var: "redis_master_6379_password"
    #         down_after_milliseconds: 30000
    #         failover_timeout: 180000
    
*   **Notes**: Actual instance definitions (ports, roles) would typically be in Ansible inventory or `group_vars`/`host_vars`. This file defines defaults and structure for more complex vars. Passwords *must* be fetched from Ansible Vault or HashiCorp Vault using `lookup` plugins in templates.

#### 4.4.2. `ansible_integration/templates/redis.conf.j2`
*   **Description**: Jinja2 template for `redis.conf`.
*   **Purpose**: Automated generation of `redis.conf` by Ansible.
*   **Logic**:
    *   Uses Jinja2 variables (e.g., `{{ redis_port }}`, `{{ redis_bind_ip }}`, `{{ redis_maxmemory_mb }}`, etc.) sourced from Ansible inventory, `group_vars`, `host_vars`, and potentially `redis_config_variables.yml`.
    *   Password directive: `requirepass "{{ lookup('hashi_vault', redis_password_secret_path) }}"` or `requirepass "{{ redis_password_vault_var | default('') }}"` if using Ansible Vault directly.
    *   Conditional blocks:
        jinja
        {% if aof_enabled == "yes" %}
        appendonly yes
        appendfilename "appendonly_{{ redis_port }}.aof"
        {% else %}
        appendonly no
        {% endif %}

        {% if cluster_enabled == "yes" %}
        cluster-enabled yes
        cluster-config-file nodes-{{ redis_port }}.conf
        cluster-node-timeout {{ cluster_node_timeout | default(15000) }}
        {% if announce_ip is defined %}
        cluster-announce-ip {{ announce_ip }}
        cluster-announce-port {{ redis_port }}
        cluster-announce-bus-port {{ cluster_bus_port | default(redis_port + 10000) }}
        {% endif %}
        {% endif %}

        {% if role == "slave" and master_ip is defined and master_port is defined %}
        replicaof {{ master_ip }} {{ master_port }}
        {% if master_password_vault_var is defined %}
        masterauth "{{ lookup('hashi_vault', master_password_vault_var) }}"
        {% endif %}
        {% endif %}
        
    *   Loops for RDB save points if defined as a list in vars.

#### 4.4.3. `ansible_integration/templates/sentinel.conf.j2`
*   **Description**: Jinja2 template for `sentinel.conf`.
*   **Purpose**: Automated generation of `sentinel.conf` by Ansible.
*   **Logic**:
    *   Uses Jinja2 variables for Sentinel specific settings: `{{ sentinel_port }}`, `{{ sentinel_logfile_path }}`, `{{ sentinel_pidfile_path }}`, `{{ announce_ip | default(ansible_default_ipv4.address) }}`.
    *   Loops through a list of monitored masters (defined in Ansible vars):
        jinja
        {% for monitor_item in sentinel_monitors %}
        sentinel monitor {{ monitor_item.name }} {{ monitor_item.ip }} {{ monitor_item.port }} {{ monitor_item.quorum }}
        sentinel down-after-milliseconds {{ monitor_item.name }} {{ monitor_item.down_after_milliseconds | default(sentinel_default_down_after_ms) }}
        sentinel parallel-syncs {{ monitor_item.name }} 1
        sentinel failover-timeout {{ monitor_item.name }} {{ monitor_item.failover_timeout | default(sentinel_default_failover_timeout_ms) }}
        {% if monitor_item.auth_pass_vault_var is defined %}
        sentinel auth-pass {{ monitor_item.name }} "{{ lookup('hashi_vault', monitor_item.auth_pass_vault_var) }}"
        {% endif %}
        {% endfor %}
        

## 5. Interfaces
This repository primarily provides configuration files and scripts.
*   **Shell Scripts**: Command-line interfaces as described in their respective sections (e.g., `./setup_redis_standalone.sh --port ...`).
*   **Lua Scripts**: Executed via Redis `EVAL` or `EVALSHA` commands. Interface defined by `KEYS` and `ARGV` parameters.
*   **Ansible**: Consumes `.yml` vars files and `.j2` templates as part of Ansible playbook execution.

## 6. Security Considerations
*   **Password Protection**: `redis.conf.template` and `sentinel.conf.template` include `requirepass` and `sentinel auth-pass` directives. Passwords must be strong and managed via Ansible Vault or HashiCorp Vault, never hardcoded or in plaintext in Git.
*   **Network Binding**: `bind` directive in `redis.conf.template` should be configured to listen only on trusted network interfaces. `protected-mode yes` is default.
*   **Command Renaming**: Consider renaming dangerous commands (e.g., `CONFIG`, `FLUSHALL`, `FLUSHDB`) in production using the `rename-command` directive in `redis.conf`. This needs to be coordinated with any tools or scripts that might use these commands.
*   **File Permissions**: Scripts creating directories and configuration files must set restrictive permissions (e.g., readable only by the `redis` user).
*   **Lua Script Security**: `lua-time-limit` is set to prevent long-running scripts. Lua scripts should be reviewed for potential security vulnerabilities if they accept dynamic user input (though these scripts primarily take predefined arguments).
*   **Principle of Least Privilege**: The `redis` user should run with minimal necessary privileges.

## 7. Deployment and Operational Considerations
*   **Automation**: Ansible is the primary tool for deploying and configuring Redis in staging and production environments using the artifacts from this repository.
*   **Idempotency**: Setup scripts and Ansible playbooks should be idempotent to allow safe re-application.
*   **Monitoring**: Redis instances should be monitored using tools like Prometheus with `redis_exporter`. Sentinel instances also expose metrics.
*   **Logging**: Standardized logging from utility scripts (`utils.sh`) aids troubleshooting. Redis server logs and Sentinel logs should be aggregated.
*   **Service Management**: `manage_service.sh` provides a basic way to control services, but in production, `systemd` or other robust service managers managed by Ansible are preferred.
*   **Backup/Restore**: While this repository focuses on configuration, persistence settings (RDB/AOF) are crucial. Actual backup procedures (e.g., copying RDB files, AOF files) are outside this repository's scope but depend on these configurations.
*   **Updates/Patching**: Redis server versions should be kept up-to-date. Configuration changes should be managed via updates to templates/variables and rolled out via Ansible.

## 8. Scalability and Performance
*   **Memory Management**: `maxmemory` and `maxmemory-policy` are critical. `allkeys-lru` is suitable for session and general cache.
*   **Clustering**: `setup_redis_cluster_nodes.sh` provides a basis for a scalable Redis Cluster.
*   **Sentinel HA**: `setup_redis_sentinel_topology.sh` sets up a high-availability master-slave-sentinel topology.
*   **Connection Pooling**: Applications connecting to Redis should use connection pooling on the client-side to manage connections efficiently.
*   **Lua Scripts**: Using server-side Lua scripts for complex atomic operations reduces network round-trips and improves performance for those specific operations.

## 9. Future Considerations
*   Support for Redis 7+ features (e.g., ACL improvements, Sharded Pub/Sub if it becomes relevant).
*   More sophisticated Lua scripts for advanced caching strategies or Pub/Sub filtering.
*   Enhanced Ansible roles with more granular control and testing.
*   Integration with TLS for Redis connections.
*   Automated testing for shell scripts using a framework like `bats`.