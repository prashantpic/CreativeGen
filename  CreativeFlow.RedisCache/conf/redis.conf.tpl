# CreativeFlow.RedisCache - Redis Server Configuration Template
# This template is managed by Ansible. Do not edit directly.
#
# See redis.io/topics/config for the full list of options.

# --- General ---
# The port Redis will listen on.
port {{ REDIS_PORT | default(6379) }}

# The IP address to bind to. Default is 127.0.0.1 (localhost).
# For production, this should be set to the server's private IP address.
# Using 0.0.0.0 is insecure as it listens on all available network interfaces.
bind {{ REDIS_BIND_IP | default("127.0.0.1") }}

# When running in protected mode, Redis only replies to commands from clients
# connected via Unix sockets, and from clients connected via TCP to the
# loopback addresses 127.0.0.1 and ::1.
protected-mode {{ REDIS_PROTECTED_MODE | default("yes") }}

# Run as a background process.
daemonize {{ REDIS_DAEMONIZE | default("yes") }}

# When daemonized, Redis writes a PID file in a configured location.
pidfile /var/run/redis/redis_server_{{ REDIS_PORT | default(6379) }}.pid

# Specify the log file name. Also the empty string can be used to force
# Redis to log on the standard output.
logfile /var/log/redis/redis_server_{{ REDIS_PORT | default(6379) }}.log

# Set the number of databases. The default database is DB 0.
databases {{ REDIS_DATABASES | default(16) }}


# --- Snapshots (RDB) ---
# Defines the conditions under which Redis will save the dataset to disk.
# save <seconds> <changes>
# Will save the DB if both the given number of seconds and the given
# number of write operations against the DB occurred.
save 900 1
save 300 10
save 60 10000

# The filename where to dump the RDB database.
dbfilename dump_{{ REDIS_PORT | default(6379) }}.rdb

# Compress string objects using LZF when dumping .rdb databases.
rdbcompression {{ REDIS_RDB_COMPRESSION | default("yes") }}

# The working directory.
# The RDB file and the AOF file will be created inside this directory.
dir /var/lib/redis/{{ REDIS_PORT | default(6379) }}


# --- Append Only Mode (AOF) ---
# AOF persistence logs every write operation received by the server.
# These are played again at server startup, reconstructing the original dataset.
appendonly {{ REDIS_AOF_ENABLED | default("no") }}

# The name of the append only file.
appendfilename "appendonly_{{ REDIS_PORT | default(6379) }}.aof"

# The fsync() policy.
# 'always': fsync every time new commands are appended to the AOF. Very slow, very safe.
# 'everysec': fsync every second. Fast enough, and you can lose only 1 second of data.
# 'no': Let the OS handle fsync. Fastest, but least safe.
appendfsync {{ REDIS_AOF_FSYNC_POLICY | default("everysec") }}


# --- Security ---
# Require clients to issue AUTH <password> before being able to execute
# other commands. This is a critical security measure.
# The placeholder {{ REDIS_PASSWORD }} MUST be injected by Ansible from a secure vault.
requirepass {{ REDIS_PASSWORD }}


# --- Clients ---
# Set the max number of connected clients at the same time.
maxclients {{ REDIS_MAX_CLIENTS | default(10000) }}


# --- Memory Management ---
# Set a memory usage limit to the specified amount of bytes.
# When the memory limit is reached Redis will try to remove keys
# according to the eviction policy selected.
# e.g., 2gb, 512mb
# The placeholder {{ REDIS_MAX_MEMORY }} MUST be injected by Ansible based on DEP-001.
maxmemory {{ REDIS_MAX_MEMORY }}

# How Redis will select what to remove when maxmemory is reached.
# volatile-lru -> remove keys with an expire set using an LRU algorithm.
# allkeys-lru -> remove any key using an LRU algorithm.
# volatile-lfu -> remove keys with an expire set using an LFU algorithm.
# allkeys-lfu -> remove any key using an LFU algorithm.
# volatile-random -> remove a random key with an expire set.
# allkeys-random -> remove a random key, any key.
# volatile-ttl -> remove the key with the nearest expire time (minor TTL).
# noeviction -> don't evict anything, just return errors on write commands.
maxmemory-policy {{ REDIS_MAXMEMORY_POLICY | default("allkeys-lru") }}


# --- Event Notification (Keyspace Notifications) ---
# Specify which events to notify clients about. Events are delivered via Pub/Sub.
# K     Keyspace events, published with __keyspace@<db>__ prefix.
# E     Keyevent events, published with __keyevent@<db>__ prefix.
# g     Generic commands (non-type specific) like DEL, EXPIRE, RENAME, ...
# $     String commands
# l     List commands
# s     Set commands
# h     Hash commands
# z     Sorted set commands
# x     Expired events (events generated every time a key expires)
# e     Evicted events (events generated when a key is evicted for maxmemory)
# A     Alias for "g$lshzxe", so all the events.
#
# "KEA" is a common default for "all events".
notify-keyspace-events {{ REDIS_KEYSPACE_EVENTS | default("KEA") }}