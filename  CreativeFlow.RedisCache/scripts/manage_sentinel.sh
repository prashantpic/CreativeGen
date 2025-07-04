#!/bin/bash
#
# CreativeFlow.RedisCache - manage_sentinel.sh
#
# Automates the start, stop, restart, and status check operations for a
# Redis Sentinel instance.
#
# Usage:
#   ./manage_sentinel.sh <start|stop|restart|status> <config_file> <pid_file> [port] [password]
#
# Example:
#   ./manage_sentinel.sh start /etc/redis/sentinel.conf /var/run/redis/sentinel_26379.pid 26379 mysecretpassword
#

# Source common environment variables and functions
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
source "${SCRIPT_DIR}/common_env.sh"

# --- Input Parameter Validation ---
if [ "$#" -lt 3 ]; then
    log_error "Usage: $0 <start|stop|restart|status> <config_file> <pid_file> [port] [password]"
    exit 1
fi

ACTION="$1"
CONFIG_FILE="$2"
PID_FILE="$3"
PORT="${4:-26379}"
PASSWORD="$5"

# --- Dependency Check ---
# redis-sentinel might be a symlink to redis-server
check_command_exists "redis-sentinel"
check_command_exists "${REDIS_CLI_PATH}"

# --- Helper Functions ---
is_running() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null; then
            return 0 # Process is running
        fi
    fi
    return 1 # Process is not running
}

# Construct redis-cli command with optional password
build_cli_command() {
    local cmd="${REDIS_CLI_PATH} -p ${PORT}"
    if [ -n "$PASSWORD" ]; then
        cmd="${cmd} -a ${PASSWORD}"
    fi
    echo "$cmd"
}

# --- Main Logic ---

case "$ACTION" in
    start)
        log_info "Attempting to start Redis Sentinel on port ${PORT}..."
        if is_running; then
            log_info "Redis Sentinel is already running with PID $(cat "$PID_FILE")."
            exit 0
        fi

        if [ ! -f "$CONFIG_FILE" ]; then
            log_error "Configuration file not found: ${CONFIG_FILE}"
            exit 1
        fi

        # Start the sentinel
        # Some systems use 'redis-server <conf> --sentinel', others use 'redis-sentinel <conf>'
        if grep -q "sentinel monitor" "$CONFIG_FILE"; then
            redis-sentinel "$CONFIG_FILE"
        else
            log_error "The provided config file does not appear to be a Sentinel configuration."
            exit 1
        fi
        
        # Verify startup
        sleep 2
        if is_running; then
            log_info "Redis Sentinel started successfully with PID $(cat "$PID_FILE")."
            # Final check with PING
            CLI_CMD=$(build_cli_command)
            if ${CLI_CMD} PING | grep -q "PONG"; then
                log_info "Sentinel is responsive (PONG received)."
                exit 0
            else
                log_error "Sentinel started but is not responsive to PING."
                exit 1
            fi
        else
            log_error "Failed to start Redis Sentinel. Check logs for details."
            exit 1
        fi
        ;;

    stop)
        log_info "Attempting to stop Redis Sentinel on port ${PORT}..."
        if ! is_running; then
            log_info "Redis Sentinel is not running."
            exit 0
        fi

        PID=$(cat "$PID_FILE")
        CLI_CMD=$(build_cli_command)

        log_info "Attempting graceful shutdown with SHUTDOWN..."
        ${CLI_CMD} SHUTDOWN

        # Wait for the process to terminate
        TIMEOUT=15
        while [ $TIMEOUT -gt 0 ]; do
            if ! is_running; then
                log_info "Redis Sentinel with PID ${PID} stopped gracefully."
                exit 0
            fi
            sleep 1
            TIMEOUT=$((TIMEOUT - 1))
        done

        # If graceful shutdown failed, force kill
        log_error "Graceful shutdown failed. Sending SIGTERM to PID ${PID}."
        kill "$PID"
        sleep 2

        if is_running; then
            log_error "Failed to stop Redis Sentinel with PID ${PID}. Manual intervention may be required."
            exit 1
        else
            log_info "Redis Sentinel stopped successfully."
            exit 0
        fi
        ;;

    restart)
        log_info "Attempting to restart Redis Sentinel on port ${PORT}..."
        "$0" stop "$CONFIG_FILE" "$PID_FILE" "$PORT" "$PASSWORD"
        sleep 2
        "$0" start "$CONFIG_FILE" "$PID_FILE" "$PORT" "$PASSWORD"
        ;;

    status)
        log_info "Checking status of Redis Sentinel on port ${PORT}..."
        if is_running; then
            PID=$(cat "$PID_FILE")
            log_info "Redis Sentinel is running with PID ${PID}."

            CLI_CMD=$(build_cli_command)
            RESPONSE=$(${CLI_CMD} PING)
            
            if [[ "$RESPONSE" == "PONG" ]]; then
                log_info "Sentinel is responsive. PING -> PONG."
                exit 0
            else
                log_error "Sentinel is running but not responding to PING. Response: ${RESPONSE}"
                exit 1
            fi
        else
            log_info "Redis Sentinel is not running."
            exit 3 # Nagios-style UNKNOWN/NOT_RUNNING status
        fi
        ;;

    *)
        log_error "Invalid action: ${ACTION}"
        log_error "Usage: $0 <start|stop|restart|status> <config_file> <pid_file> [port] [password]"
        exit 1
        ;;
esac