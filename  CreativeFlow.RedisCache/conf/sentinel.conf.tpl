# CreativeFlow.RedisCache - Redis Sentinel Configuration Template
# This template is managed by Ansible. Do not edit directly.

# The port that this sentinel instance will run on.
port {{ SENTINEL_PORT | default(26379) }}

# Run as a background process.
daemonize {{ SENTINEL_DAEMONIZE | default("yes") }}

# PID file path.
pidfile /var/run/redis/sentinel_{{ SENTINEL_PORT | default(26379) }}.pid

# Log file path.
logfile /var/log/redis/sentinel_{{ SENTINEL_PORT | default(26379) }}.log

# Working directory.
dir /tmp

# --- Monitor Configuration ---
# Tells Sentinel to monitor a master instance.
# sentinel monitor <master-name> <ip> <port> <quorum>
#
# <master-name>: A name for the master (e.g., "creativeflow-master").
# <ip>: The IP address of the master.
# <port>: The port of the master.
# <quorum>: The number of Sentinels that need to agree the master is down
#           to start a failover.
sentinel monitor {{ SENTINEL_MASTER_NAME }} {{ SENTINEL_MASTER_IP }} {{ SENTINEL_MASTER_PORT }} {{ SENTINEL_QUORUM }}

# --- Failover Timing and Behavior ---
# The time in milliseconds an instance should not be reachable (either does not
# reply to PING or replies with an error) for a Sentinel to consider it in
# S_DOWN state (Subjectively Down).
sentinel down-after-milliseconds {{ SENTINEL_MASTER_NAME }} {{ SENTINEL_DOWN_AFTER_MS | default(30000) }}

# The number of replicas that can be reconfigured to use the new master after a
# failover at the same time. A low number is safer for data transfer, but slower.
sentinel parallel-syncs {{ SENTINEL_MASTER_NAME }} {{ SENTINEL_PARALLEL_SYNCS | default(1) }}

# The timeout in milliseconds for failover operations.
# If a failover is not completed within this time, it's considered failed.
sentinel failover-timeout {{ SENTINEL_MASTER_NAME }} {{ SENTINEL_FAILOVER_TIMEOUT | default(180000) }}

# --- Security for Monitored Master ---
# If the master being monitored is password-protected, Sentinel needs the
# password to connect.
# The placeholder {{ SENTINEL_MASTER_PASSWORD }} MUST be injected by Ansible from a secure vault.
{% if SENTINEL_MASTER_PASSWORD %}
sentinel auth-pass {{ SENTINEL_MASTER_NAME }} {{ SENTINEL_MASTER_PASSWORD }}
{% endif %}

# --- Security for Sentinel Itself (Redis 6.2+ ACLs recommended) ---
# To secure the Sentinel instance itself, preventing unauthorized clients
# from reconfiguring it.
# The placeholder {{ SENTINEL_PASSWORD }} MUST be injected by Ansible from a secure vault.
{% if SENTINEL_PASSWORD %}
# Requires clients to authenticate to this Sentinel instance.
requirepass {{ SENTINEL_PASSWORD }}

# Defines an ACL user for other Sentinels to connect with.
sentinel sentinel-user {{ SENTINEL_USER | default("default") }} password {{ SENTINEL_PASSWORD }} +all
{% endif %}