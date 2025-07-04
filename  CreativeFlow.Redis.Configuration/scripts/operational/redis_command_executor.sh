#!/bin/bash
set -euo pipefail

# Securely execute Redis commands using redis-cli.
# A wrapper to handle connection parameters consistently.
# Based on SDS section 4.2.7.

# Source utility functions
UTILS_PATH="$(dirname "$0")/../common/utils.sh"
source "$UTILS_PATH"

verify_command "redis-cli" || exit 1

# --- Defaults ---
HOST="127.0.0.1"
PORT="6379"
PASSWORD=""
COMMAND=""

usage() {
    echo "Usage: $0 --host <host> --port <port> --command \"<COMMAND> [ARGS...]\" [--password <pass>]"
    echo "  --host:      Redis server hostname (default: 127.0.0.1)"
    echo "  --port:      Redis server port (default: 6379)"
    echo "  --command:   The Redis command to execute (required, must be quoted)"
    echo "  --password:  Redis password (optional, can also use REDIS_PASSWORD env var)"
    exit 1
}

# --- Parse arguments ---
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --host) HOST="$2"; shift ;;
        --port) PORT="$2"; shift ;;
        --password) PASSWORD="$2"; shift ;;
        --command) COMMAND="$2"; shift ;;
        --help) usage ;;
        *) log_error "Unknown parameter passed: $1"; usage ;;
    esac
    shift
done

# --- Validate arguments ---
if [ -z "$COMMAND" ]; then
    log_error "The --command argument is required."
    usage
fi

# Prefer provided password, but fall back to environment variable for security
if [ -z "$PASSWORD" ] && [ -n "${REDIS_PASSWORD:-}" ]; then
    PASSWORD="$REDIS_PASSWORD"
    log_info "Using password from REDIS_PASSWORD environment variable."
fi

# --- Construct and execute command ---
CLI_ARGS=("-h" "$HOST" "-p" "$PORT")

if [ -n "$PASSWORD" ]; then
    # Pass password via environment variable to avoid it appearing in process list
    export REDISCLI_AUTH="$PASSWORD"
    log_info "Executing command on $HOST:$PORT: '$COMMAND' (with password)"
else
    log_info "Executing command on $HOST:$PORT: '$COMMAND' (without password)"
fi

# Execute the command, passing the command string as separate arguments to redis-cli
# This is safer than using eval. The "bash -c" trick ensures the command string is
# properly parsed with its arguments.
bash -c "redis-cli ${CLI_ARGS[*]} $COMMAND"

# Unset the env var after use
if [ -n "${REDISCLI_AUTH:-}" ]; then
    unset REDISCLI_AUTH
fi