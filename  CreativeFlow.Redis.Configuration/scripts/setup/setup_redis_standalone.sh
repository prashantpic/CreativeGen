#!/bin/bash
set -euo pipefail

# Sets up and configures a standalone Redis instance.
# Creates necessary directories and generates a config file from template.
# Based on SDS section 4.2.3.

# Source utility functions
UTILS_PATH="$(dirname "$0")/../common/utils.sh"
if [ ! -f "$UTILS_PATH" ]; then
    echo "[ERROR] $(date '+%Y-%m-%d %H:%M:%S'): Utility script not found at $UTILS_PATH" >&2
    exit 1
fi
source "$UTILS_PATH"

# --- Default values ---
PORT="6379"
PASSWORD=""
MAXMEMORY_MB="512"
AOF_ENABLED="yes"
BIND_IP="127.0.0.1"
CONFIG_DIR="/etc/redis"
DATA_DIR_BASE="/var/lib/redis"
LOG_DIR="/var/log/redis"

# --- Usage function ---
usage() {
    echo "Usage: $0 --port <port> --password <pass> --maxmemory <MB> [--aof <yes|no>] [--bind-ip <ip>] [--config-dir <dir>] [--data-dir <dir>] [--log-dir <dir>]"
    echo "  --port:        Redis server port (required)"
    echo "  --password:    Redis password (required)"
    echo "  --maxmemory:   Max memory in MB (required)"
    echo "  --aof:         Enable AOF persistence (yes|no, default: yes)"
    echo "  --bind-ip:     IP address to bind to (default: 127.0.0.1)"
    echo "  --config-dir:  Directory for config files (default: /etc/redis)"
    echo "  --data-dir:    Base directory for data files (default: /var/lib/redis)"
    echo "  --log-dir:     Directory for log files (default: /var/log/redis)"
    exit 1
}

# --- Parse command-line arguments ---
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --port) PORT="$2"; shift ;;
        --password) PASSWORD="$2"; shift ;;
        --maxmemory) MAXMEMORY_MB="$2"; shift ;;
        --aof) AOF_ENABLED="$2"; shift ;;
        --bind-ip) BIND_IP="$2"; shift ;;
        --config-dir) CONFIG_DIR="$2"; shift ;;
        --data-dir) DATA_DIR_BASE="$2"; shift ;;
        --log-dir) LOG_DIR="$2"; shift ;;
        --help) usage ;;
        *) log_error "Unknown parameter passed: $1"; usage ;;
    esac
    shift
done

# --- Validate inputs ---
if [ -z "$PORT" ] || [ -z "$PASSWORD" ] || [ -z "$MAXMEMORY_MB" ]; then
    log_error "Missing required arguments: --port, --password, and --maxmemory are all required."
    usage
fi
is_valid_port "$PORT" || exit 1
is_valid_ip "$BIND_IP" || exit 1
if ! [[ "$MAXMEMORY_MB" =~ ^[0-9]+$ ]]; then
    log_error "Max memory must be an integer."
    exit 1
fi
if [[ "$AOF_ENABLED" != "yes" && "$AOF_ENABLED" != "no" ]]; then
    log_error "AOF must be 'yes' or 'no'."
    exit 1
fi

log_info "Setting up standalone Redis on port $PORT..."

# --- Create directories ---
DATA_DIR="${DATA_DIR_BASE}/${PORT}"
log_info "Creating directories..."
# Use sudo if not running as root, as these are system directories
SUDO_CMD=""
if [ "$(id -u)" -ne 0 ]; then
    SUDO_CMD="sudo"
    log_info "Not running as root, will use 'sudo' for directory operations."
fi
$SUDO_CMD mkdir -p "$CONFIG_DIR" "$DATA_DIR" "$LOG_DIR"

# In a real scenario, you would set ownership here:
# $SUDO_CMD chown -R redis:redis "$CONFIG_DIR" "$DATA_DIR_BASE" "$LOG_DIR"
# log_info "Set ownership for redis user (simulated)."

# --- Generate configuration ---
SCRIPT_DIR=$(dirname "$0")
TEMPLATE_FILE="${SCRIPT_DIR}/../../config/redis.conf.template"
OUTPUT_CONFIG="${CONFIG_DIR}/redis_${PORT}.conf"

log_info "Generating configuration file at $OUTPUT_CONFIG..."

# Prepare key-value pairs for replacement
CONFIG_VARS=(
    "REDIS_PORT=$PORT"
    "REDIS_PASSWORD=$PASSWORD"
    "MAXMEMORY_MB=$MAXMEMORY_MB"
    "AOF_ENABLED=$AOF_ENABLED"
    "REDIS_BIND_IP=$BIND_IP"
)

# Call apply_config.sh, potentially with sudo if target dir requires it
if [ "$SUDO_CMD" == "sudo" ]; then
    # Create a temporary file and then move it with sudo
    TMP_CONFIG_FILE=$(mktemp)
    "${SCRIPT_DIR}/apply_config.sh" "$TEMPLATE_FILE" "$TMP_CONFIG_FILE" "${CONFIG_VARS[@]}"
    $SUDO_CMD mv "$TMP_CONFIG_FILE" "$OUTPUT_CONFIG"
    $SUDO_CMD chown redis:redis "$OUTPUT_CONFIG"
else
    # Running as root, can write directly
    "${SCRIPT_DIR}/apply_config.sh" "$TEMPLATE_FILE" "$OUTPUT_CONFIG" "${CONFIG_VARS[@]}"
fi

log_info "Standalone Redis setup complete."
log_info "Config file created: $OUTPUT_CONFIG"
log_info "To start the service (if not managed by systemd): redis-server $OUTPUT_CONFIG"
exit 0