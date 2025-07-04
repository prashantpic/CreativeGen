#
# CreativeFlow.MinIO.Configuration - Common Shell Utilities
#
# This script contains common shell functions for logging, error handling,
# and environment checks. It is intended to be sourced by other scripts.
#

# Prints an informational message with a timestamp.
# Usage: log_info "Your message here"
log_info() {
    local message="$1"
    echo "$(date '+%Y-%m-%d %H:%M:%S') INFO: ${message}"
}

# Prints an error message with a timestamp to STDERR.
# Usage: log_error "Your error message here"
log_error() {
    local message="$1"
    echo "$(date '+%Y-%m-%d %H:%M:%S') ERROR: ${message}" >&2
}

# Checks if a list of environment variables are set and non-empty.
# Exits the script with an error if any variable is missing.
# Usage: check_env_vars "VAR1" "VAR2" "VAR3"
check_env_vars() {
    for var_name in "$@"; do
        if [ -z "${!var_name}" ]; then
            log_error "Required environment variable '${var_name}' is not set or is empty. Please check your 'set_env.sh' file."
            exit 1
        fi
    done
}

# Checks if the `mc` command is available in the system's PATH.
# Exits the script with an error if it's not found.
# Usage: check_mc_command
check_mc_command() {
    if ! command -v mc &> /dev/null; then
        log_error "'mc' (MinIO Client) command not found. Please install it and ensure it is in your system's PATH."
        exit 1
    fi
}