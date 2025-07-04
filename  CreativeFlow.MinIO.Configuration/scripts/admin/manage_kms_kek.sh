#!/bin/bash
#
# CreativeFlow.MinIO.Configuration - KMS Key Encryption Key (KEK) Management
#
# Requirement Mapping: SEC-003, REQ-DA-010
#
# This script manages KEKs for server-side encryption with an external KMS.
# IMPORTANT: The MinIO server MUST be pre-configured to connect to an
# external KMS (e.g., HashiCorp Vault) for these commands to work.
#

set -e
set -o pipefail

# Source common utilities
source "$(dirname "$0")/../common_utils.sh"

# --- Functions ---
usage() {
    echo "Usage: $0 <ACTION> [ARGUMENTS...]"
    echo ""
    echo "Manages Key Encryption Keys (KEK) with an external KMS."
    echo ""
    echo "Actions:"
    echo "  create <KEK_NAME>    - Creates a new KEK with the given name (key-id)."
    echo "  status <KEK_NAME>    - Gets the status of a specific KEK."
    echo "  list                 - Lists all KEKs known to MinIO."
    echo ""
    echo "Example:"
    echo "  $0 create my-app-kek"
    echo "  $0 status my-app-kek"
    exit 1
}

# --- Main Script Logic ---

# Check for sourced environment and mc command
if [ -f "$(dirname "$0")/../../set_env.sh" ]; then
    source "$(dirname "$0")/../../set_env.sh"
fi
check_env_vars "MINIO_ALIAS_NAME"
check_mc_command

# Check for action argument
if [ -z "$1" ]; then
    log_error "No action specified."
    usage
fi

ACTION="$1"
shift

log_info "Executing KMS KEK action: ${ACTION}..."

case "${ACTION}" in
    create)
        [ "$#" -ne 1 ] && log_error "Usage: create <KEK_NAME>" && exit 1
        KEK_NAME="$1"
        log_info "Creating KEK '${KEK_NAME}' on '${MINIO_ALIAS_NAME}'..."
        if mc admin kms key create "${MINIO_ALIAS_NAME}" --key-id "${KEK_NAME}"; then
            log_info "KEK '${KEK_NAME}' created successfully."
        else
            log_error "Failed to create KEK '${KEK_NAME}'. Check KMS configuration and connection."
            exit 1
        fi
        ;;
    status)
        [ "$#" -ne 1 ] && log_error "Usage: status <KEK_NAME>" && exit 1
        KEK_NAME="$1"
        log_info "Getting status for KEK '${KEK_NAME}' on '${MINIO_ALIAS_NAME}'..."
        mc admin kms key status "${MINIO_ALIAS_NAME}" --key-id "${KEK_NAME}"
        ;;
    list)
        [ "$#" -ne 0 ] && log_error "Usage: list" && exit 1
        log_info "Listing KEKs on '${MINIO_ALIAS_NAME}'..."
        mc admin kms key ls "${MINIO_ALIAS_NAME}"
        ;;
    *)
        log_error "Invalid action: ${ACTION}"
        usage
        ;;
esac

log_info "KMS KEK action '${ACTION}' completed."
log_info "Reminder: MinIO server must be properly configured to communicate with your external KMS."