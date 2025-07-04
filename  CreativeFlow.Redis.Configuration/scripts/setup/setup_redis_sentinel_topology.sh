#!/bin/bash
set -euo pipefail

# Configures a Redis master, one or more slaves, and a set of Sentinel instances.
# NOTE: This script is for demonstration and config generation. In a real-world scenario,
# Ansible or another tool would deploy these configurations to their respective hosts.
# Based on SDS section 4.2.4.

# Source utility functions
UTILS_PATH="$(dirname "$0")/../common/utils.sh"
source "$UTILS_PATH"

# --- Default Configuration (can be overridden by args) ---
MASTER_IP="127.0.0.1"
MASTER_PORT="6379"
MASTER_PASS=""
MASTER_NAME="mymaster"
SLAVE_NODES="127.0.0.1:6380" # Space-separated list: "ip1:port1 ip2:port2"
SENTINEL_NODES="127.0.0.1:26379 127.0.0.1:26380 127.0.0.1:26381" # Space-separated list
SENTINEL_QUORUM="2"
CONFIG_BASE_DIR="/tmp/redis-ha-topology"
DOWN_AFTER_MS=5000
FAILOVER_TIMEOUT_MS=10000

usage() {
    echo "Usage: $0 --master-ip <ip> --master-port <port> --master-pass <pass> --slave-nodes \"...\" --sentinel-nodes \"...\" [--sentinel-quorum <N>] [--config-base-dir <dir>]"
    exit 1
}

# --- Parse command-line arguments (basic) ---
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --master-ip) MASTER_IP="$2"; shift ;;
        --master-port) MASTER_PORT="$2"; shift ;;
        --master-pass) MASTER_PASS="$2"; shift ;;
        --slave-nodes) SLAVE_NODES="$2"; shift ;;
        --sentinel-nodes) SENTINEL_NODES="$2"; shift ;;
        --sentinel-quorum) SENTINEL_QUORUM="$2"; shift ;;
        --config-base-dir) CONFIG_BASE_DIR="$2"; shift ;;
        *) log_error "Unknown parameter passed: $1"; usage ;;
    esac
    shift
done

if [ -z "$MASTER_PASS" ]; then
    log_error "Master password (--master-pass) is required."
    exit 1
fi

log_info "--- Setting up Redis Sentinel HA Topology configuration in '$CONFIG_BASE_DIR' ---"
rm -rf "$CONFIG_BASE_DIR"
mkdir -p "$CONFIG_BASE_DIR"

# --- 1. Master Setup ---
log_info "Generating config for Master on ${MASTER_IP}:${MASTER_PORT}"
MASTER_CONFIG="${CONFIG_BASE_DIR}/redis_master_${MASTER_PORT}.conf"
"$(dirname "$0")/apply_config.sh" "$(dirname "$0")/../../config/redis.conf.template" "$MASTER_CONFIG" \
    "REDIS_PORT=$MASTER_PORT" \
    "REDIS_PASSWORD=$MASTER_PASS" \
    "REDIS_BIND_IP=$MASTER_IP" \
    "AOF_ENABLED=yes" \
    "MAXMEMORY_MB=1024"

# --- 2. Slave Setup ---
for slave_node in $SLAVE_NODES; do
    SLAVE_IP=$(echo "$slave_node" | cut -d':' -f1)
    SLAVE_PORT=$(echo "$slave_node" | cut -d':' -f2)
    log_info "Generating config for Slave on ${SLAVE_IP}:${SLAVE_PORT}"
    
    SLAVE_CONFIG="${CONFIG_BASE_DIR}/redis_slave_${SLAVE_PORT}.conf"
    
    "$(dirname "$0")/apply_config.sh" "$(dirname "$0")/../../config/redis.conf.template" "$SLAVE_CONFIG" \
        "REDIS_PORT=$SLAVE_PORT" \
        "REDIS_PASSWORD=$MASTER_PASS" \
        "REDIS_BIND_IP=$SLAVE_IP" \
        "AOF_ENABLED=yes" \
        "MAXMEMORY_MB=1024" \
        "IF_SLAVE_MODE##replicaof=$MASTER_IP $MASTER_PORT" \
        "IF_SLAVE_MODE##masterauth=$MASTER_PASS"
done

# --- 3. Sentinel Setup ---
for sentinel_node in $SENTINEL_NODES; do
    SENTINEL_IP=$(echo "$sentinel_node" | cut -d':' -f1)
    SENTINEL_PORT=$(echo "$sentinel_node" | cut -d':' -f2)
    log_info "Generating config for Sentinel on ${SENTINEL_IP}:${SENTINEL_PORT}"

    SENTINEL_CONFIG="${CONFIG_BASE_DIR}/sentinel_${SENTINEL_PORT}.conf"

    "$(dirname "$0")/apply_config.sh" "$(dirname "$0")/../../config/sentinel.conf.template" "$SENTINEL_CONFIG" \
        "SENTINEL_PORT=$SENTINEL_PORT" \
        "MASTER_NAME=$MASTER_NAME" \
        "MASTER_IP=$MASTER_IP" \
        "MASTER_PORT=$MASTER_PORT" \
        "QUORUM=$SENTINEL_QUORUM" \
        "MASTER_PASSWORD=$MASTER_PASS" \
        "DOWN_AFTER_MS=$DOWN_AFTER_MS" \
        "FAILOVER_TIMEOUT_MS=$FAILOVER_TIMEOUT_MS" \
        "ANNOUNCE_IP=$SENTINEL_IP"
done

log_info "--- Topology Configuration Generation Complete ---"
log_info "Configuration files are located in '$CONFIG_BASE_DIR'."
log_info "To run this demo locally (ensure ports are free):"
log_info "1. Start Master: redis-server $MASTER_CONFIG"
log_info "2. Start Slaves (example): redis-server ${CONFIG_BASE_DIR}/redis_slave_6380.conf"
log_info "3. Start Sentinels (example): redis-sentinel ${CONFIG_BASE_DIR}/sentinel_26379.conf"
log_info "Use 'redis-cli -p <port> -a <pass> INFO replication' to check status."