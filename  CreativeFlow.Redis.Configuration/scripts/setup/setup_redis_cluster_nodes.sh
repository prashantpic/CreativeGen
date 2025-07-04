#!/bin/bash
set -euo pipefail

# Configures nodes for Redis Cluster and then uses redis-cli to form the cluster.
# Based on SDS section 4.2.5.

# Source utility functions
UTILS_PATH="$(dirname "$0")/../common/utils.sh"
source "$UTILS_PATH"

verify_command "redis-cli" || exit 1

# --- Configuration (can be overridden by args) ---
NODES="127.0.0.1:7000 127.0.0.1:7001 127.0.0.1:7002 127.0.0.1:7003 127.0.0.1:7004 127.0.0.1:7005"
REPLICAS="1"
PASSWORD=""
CONFIG_BASE_DIR="/tmp/redis-cluster-demo"

usage() {
    echo "Usage: $0 --nodes \"ip1:port1 ip2:port2 ...\" --replicas <N> --password <pass> [--config-base-dir <dir>]"
    exit 1
}

# --- Parse command-line arguments (basic) ---
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --nodes) NODES="$2"; shift ;;
        --replicas) REPLICAS="$2"; shift ;;
        --password) PASSWORD="$2"; shift ;;
        --config-base-dir) CONFIG_BASE_DIR="$2"; shift ;;
        *) log_error "Unknown parameter passed: $1"; usage ;;
    esac
    shift
done

if [ -z "$PASSWORD" ]; then
    log_error "Password (--password) is required for cluster setup."
    exit 1
fi

log_info "--- Setting up Redis Cluster configuration in '$CONFIG_BASE_DIR' ---"
rm -rf "$CONFIG_BASE_DIR"
mkdir -p "$CONFIG_BASE_DIR"

NODE_LIST_FOR_CLI=""

# --- 1. Node Configuration and Startup ---
for node in $NODES; do
    NODE_IP=$(echo "$node" | cut -d':' -f1)
    NODE_PORT=$(echo "$node" | cut -d':' -f2)
    CLUSTER_BUS_PORT=$((NODE_PORT + 10000))
    NODE_DATA_DIR="${CONFIG_BASE_DIR}/data/${NODE_PORT}"
    
    log_info "Configuring Cluster Node on ${NODE_IP}:${NODE_PORT}"
    
    mkdir -p "$NODE_DATA_DIR" "${CONFIG_BASE_DIR}/log" "${CONFIG_BASE_DIR}/run"

    NODE_CONFIG="${CONFIG_BASE_DIR}/redis_cluster_${NODE_PORT}.conf"
    
    "$(dirname "$0")/apply_config.sh" "$(dirname "$0")/../../config/redis.conf.template" "$NODE_CONFIG" \
        "REDIS_PORT=$NODE_PORT" \
        "REDIS_PASSWORD=$PASSWORD" \
        "REDIS_BIND_IP=$NODE_IP" \
        "IF_CLUSTER_MODE##cluster-enabled=yes" \
        "IF_CLUSTER_MODE##cluster-config-file=nodes-${NODE_PORT}.conf" \
        "IF_CLUSTER_MODE##cluster-node-timeout=5000" \
        "IF_CLUSTER_MODE##cluster-announce-ip=${NODE_IP}" \
        "IF_CLUSTER_MODE##cluster-announce-bus-port=${CLUSTER_BUS_PORT}" \
        "AOF_ENABLED=yes" \
        "MAXMEMORY_MB=256" # Keep it small for local demo

    # Customize paths for local demo to avoid conflicts
    sed -i.bak "s|/var/lib/redis/##REDIS_PORT##|${NODE_DATA_DIR}|g" "$NODE_CONFIG"
    sed -i.bak "s|/var/log/redis/redis_##REDIS_PORT##.log|${CONFIG_BASE_DIR}/log/redis_${NODE_PORT}.log|g" "$NODE_CONFIG"
    sed -i.bak "s|/var/run/redis_##REDIS_PORT##.pid|${CONFIG_BASE_DIR}/run/redis_${NODE_PORT}.pid|g" "$NODE_CONFIG"
    rm -f "${NODE_CONFIG}.bak"

    log_info "Starting node on port $NODE_PORT..."
    redis-server "$NODE_CONFIG"

    NODE_LIST_FOR_CLI+="${NODE_IP}:${NODE_PORT} "
done

log_info "Waiting 5 seconds for all nodes to initialize..."
sleep 5

# --- 2. Form the cluster ---
log_info "Creating the cluster with ${REPLICAS} replica(s) for each master..."
# The 'yes' is piped to auto-accept the proposed cluster configuration.
# Note: For Redis 6+, the password can be supplied with -a.
# For older versions, or complex auth, you might need an `expect` script or rely on passwordless setup within a trusted network.
echo "yes" | redis-cli -a "$PASSWORD" --cluster create $NODE_LIST_FOR_CLI --cluster-replicas "$REPLICAS"

if [ $? -eq 0 ]; then
    log_info "--- Redis Cluster Setup Complete ---"
    log_info "To check cluster status: redis-cli -a $PASSWORD -p 7000 cluster info"
    log_info "To connect to cluster: redis-cli -c -a $PASSWORD -p 7000"
else
    log_error "Cluster creation failed. Check logs in ${CONFIG_BASE_DIR}/log"
fi