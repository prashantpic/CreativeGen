#!/bin/bash
#
# CreativeFlow.RedisCache - common_env.sh
#
# This script centralizes common environment variables and utility functions
# for shell scripts within this repository. It should be sourced by other scripts.
#

# --- Common Environment Variables ---

# Attempt to find redis-cli, fallback to a common path.
REDIS_CLI_PATH=$(which redis-cli || echo "/usr/local/bin/redis-cli")

# Default host if not specified by the calling script.
DEFAULT_REDIS_HOST="127.0.0.1"

# DEFAULT_REDIS_PORT will be passed as an argument or set specifically by calling scripts.
# DEFAULT_REDIS_PASSWORD will be passed as an argument if needed.


# --- Utility Functions ---

# Standardized informational logging.
# Usage: log_info "Your message here"
log_info() {
    echo "[INFO] $(date +'%Y-%m-%d %H:%M:%S') - $1"
}

# Standardized error logging.
# Usage: log_error "Your error message here"
log_error() {
    echo "[ERROR] $(date +'%Y-%m-%d %H:%M:%S') - $1" >&2
}

# Verifies if a command is available in PATH. Exits if not found.
# Usage: check_command_exists "command_name"
check_command_exists() {
    if ! command -v "$1" >/dev/null 2>&1; then
        log_error "Command '$1' not found. Please install it or check your PATH environment variable."
        exit 1
    fi
}