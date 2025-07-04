#!/bin/bash

# Common utility functions for CreativeFlow Redis scripts.
# Sourced by other scripts to provide logging, validation, and other helpers.
# Based on SDS section 4.2.1.

# Echos an info-level message with a timestamp to stdout.
# Usage: log_info "Your message here"
log_info() {
    echo "[INFO] $(date '+%Y-%m-%d %H:%M:%S'): $1"
}

# Echos an error-level message with a timestamp to stderr.
# Usage: log_error "Your error message here"
log_error() {
    echo "[ERROR] $(date '+%Y-%m-%d %H:%M:%S'): $1" >&2
}

# Verifies if a command exists in the system's PATH.
# Returns 0 if found, 1 otherwise.
# Usage: verify_command "redis-cli"
verify_command() {
    if ! command -v "$1" &> /dev/null; then
        log_error "Required command '$1' not found in PATH."
        return 1
    fi
    return 0
}

# Validates if a string is a valid IPv4 address.
# Returns 0 if valid, 1 otherwise.
# Usage: is_valid_ip "127.0.0.1"
is_valid_ip() {
    local ip=$1
    local regex="^([0-9]{1,3}\.){3}[0-9]{1,3}$"
    if [[ $ip =~ $regex ]]; then
        # Further check to ensure each octet is between 0 and 255
        IFS='.' read -r -a octets <<< "$ip"
        for octet in "${octets[@]}"; do
            if (( octet < 0 || octet > 255 )); then
                log_error "Invalid IP address: octet '$octet' out of range in '$ip'"
                return 1
            fi
        done
        return 0
    else
        log_error "Invalid IP address format: '$ip'"
        return 1
    fi
}

# Validates if a number is a valid network port (1-65535).
# Returns 0 if valid, 1 otherwise.
# Usage: is_valid_port "6379"
is_valid_port() {
    local port=$1
    if [[ "$port" =~ ^[0-9]+$ ]] && [ "$port" -ge 1 ] && [ "$port" -le 65535 ]; then
        return 0
    else
        log_error "Invalid port number: '$port'. Must be a number between 1 and 65535."
        return 1
    fi
}