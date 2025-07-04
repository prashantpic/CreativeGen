#!/bin/bash
set -euo pipefail

# Manages Redis/Sentinel services (start, stop, restart, status).
# Detects systemd but defaults to direct process management if unavailable or not configured.
# Based on SDS section 4.2.6.

# Source utility functions
UTILS_PATH="$(dirname "$0")/../common/utils.sh"
source "$UTILS_PATH"

# --- Argument Validation ---
if [ "$#" -ne 3 ]; then
    log_error "Usage: $0 <start|stop|restart|status> <redis|sentinel> <config_file_path>"
    exit 1
fi

ACTION="$1"
SERVICE_TYPE="$2"
CONFIG_FILE="$3"

if [ ! -f "$CONFIG_FILE" ]; then
    log_error "Configuration file not found: '$CONFIG_FILE'"
    exit 1
fi

# --- Determine service details ---
EXECUTABLE=""
if [ "$SERVICE_TYPE" == "redis" ]; then
    EXECUTABLE="redis-server"
elif [ "$SERVICE_TYPE" == "sentinel" ]; then
    EXECUTABLE="redis-sentinel"
else
    log_error "Invalid service type '$SERVICE_TYPE'. Must be 'redis' or 'sentinel'."
    exit 1
fi
verify_command "$EXECUTABLE" || exit 1
verify_command "grep" || exit 1
verify_command "awk" || exit 1

# --- Helper functions for direct process management ---
get_config_value() {
    grep -E "^\s*$1\s+" "$2" | awk '{print $2}' | tr -d '"' | tail -n 1
}

PORT=$(get_config_value "port" "$CONFIG_FILE")
PID_FILE=$(get_config_value "pidfile" "$CONFIG_FILE")
# For Sentinel, auth-pass is per-master. For Redis, it's requirepass.
PASSWORD=$(get_config_value "requirepass" "$CONFIG_FILE")

if [ -z "$PORT" ] || [ -z "$PID_FILE" ]; then
    log_error "Could not extract 'port' and 'pidfile' from '$CONFIG_FILE'."
    exit 1
fi

# --- Service action functions ---
do_start() {
    if is_running; then
        log_info "$SERVICE_TYPE on port $PORT is already running."
        return
    fi
    log_info "Starting $SERVICE_TYPE with config '$CONFIG_FILE'..."
    $EXECUTABLE "$CONFIG_FILE"
    sleep 2 # Give it a moment to start and write pid file
    if is_running; then
        log_info "Service started successfully with PID $(cat "$PID_FILE")."
    else
        log_error "Failed to start service. Check logs."
        exit 1
    fi
}

do_stop() {
    if ! is_running; then
        log_info "$SERVICE_TYPE on port $PORT is not running."
        return
    fi
    log_info "Stopping $SERVICE_TYPE on port $PORT (PID $(cat "$PID_FILE"))..."
    
    # Prefer clean shutdown via redis-cli if possible
    if [ "$SERVICE_TYPE" == "redis" ] && verify_command "redis-cli"; then
        SHUTDOWN_CMD="redis-cli -p $PORT"
        if [ -n "$PASSWORD" ]; then
            SHUTDOWN_CMD+=" -a $PASSWORD"
        fi
        $SHUTDOWN_CMD shutdown &> /dev/null
        sleep 2
    fi

    # Fallback or final check with kill
    if is_running; then
        log_info "Service did not shut down cleanly, sending KILL signal."
        kill "$(cat "$PID_FILE")"
    fi
    
    # Wait for process to terminate
    for _ in {1..5}; do
        if ! is_running; then
            log_info "Service stopped."
            rm -f "$PID_FILE"
            return
        fi
        sleep 1
    done
    
    log_error "Failed to stop service with PID $(cat "$PID_FILE")."
    exit 1
}

do_status() {
    if is_running; then
        log_info "$SERVICE_TYPE on port $PORT is RUNNING with PID $(cat "$PID_FILE")."
        return 0
    else
        log_info "$SERVICE_TYPE on port $PORT is STOPPED."
        return 1
    fi
}

is_running() {
    [ -f "$PID_FILE" ] && ps -p "$(cat "$PID_FILE")" > /dev/null
}

# --- Main Logic ---
# Note: systemd detection is omitted for simplicity, focusing on direct management
# as per the SDS fall-back logic. A real-world script would have `if command -v systemctl...`
case "$ACTION" in
    start)
        do_start
        ;;
    stop)
        do_stop
        ;;
    restart)
        log_info "Restarting service..."
        do_stop
        sleep 1
        do_start
        ;;
    status)
        do_status
        ;;
    *)
        log_error "Invalid action '$ACTION'. Must be start, stop, restart, or status."
        exit 1
        ;;
esac

exit 0