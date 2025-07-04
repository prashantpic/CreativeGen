#!/bin/bash
#
# CreativeFlow.MinIO.Configuration - User and Group Management Script
#
# Requirement Mapping: SEC-006
#
# This script provides a CLI to manage MinIO users and groups by wrapping
# 'mc admin user' and 'mc admin group' commands.
#

set -e
set -o pipefail

# Source common utilities
source "$(dirname "$0")/../common_utils.sh"

# --- Functions ---
usage() {
    echo "Usage: $0 <ACTION> [ARGUMENTS...]"
    echo ""
    echo "A wrapper script for managing MinIO users and groups."
    echo ""
    echo "Actions:"
    echo "  add-user <USERNAME> <PASSWORD>         - Adds a new user."
    echo "  remove-user <USERNAME>                 - Removes a user."
    echo "  list-users                             - Lists all users."
    echo "  info-user <USERNAME>                   - Shows info for a user."
    echo ""
    echo "  add-group <GROUPNAME>                  - Adds a new group."
    echo "  remove-group <GROUPNAME>               - Removes a group."
    echo "  list-groups                            - Lists all groups."
    echo "  info-group <GROUPNAME>                 - Shows info for a group."
    echo ""
    echo "  add-user-to-group <GROUPNAME> <USERNAME> - Adds a user to a group."
    echo "  remove-user-from-group <GROUPNAME> <USERNAME> - Removes a user from a group."
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

log_info "Executing action: ${ACTION}..."

case "${ACTION}" in
    add-user)
        [ "$#" -ne 2 ] && log_error "Usage: add-user <USERNAME> <PASSWORD>" && exit 1
        mc admin user add "${MINIO_ALIAS_NAME}" "$1" "$2"
        ;;
    remove-user)
        [ "$#" -ne 1 ] && log_error "Usage: remove-user <USERNAME>" && exit 1
        mc admin user rm "${MINIO_ALIAS_NAME}" "$1"
        ;;
    list-users)
        [ "$#" -ne 0 ] && log_error "Usage: list-users" && exit 1
        mc admin user ls "${MINIO_ALIAS_NAME}"
        ;;
    info-user)
        [ "$#" -ne 1 ] && log_error "Usage: info-user <USERNAME>" && exit 1
        mc admin user info "${MINIO_ALIAS_NAME}" "$1"
        ;;
    add-group)
        [ "$#" -ne 1 ] && log_error "Usage: add-group <GROUPNAME>" && exit 1
        mc admin group add "${MINIO_ALIAS_NAME}" "$1"
        ;;
    remove-group)
        [ "$#" -ne 1 ] && log_error "Usage: remove-group <GROUPNAME>" && exit 1
        mc admin group rm "${MINIO_ALIAS_NAME}" "$1"
        ;;
    list-groups)
        [ "$#" -ne 0 ] && log_error "Usage: list-groups" && exit 1
        mc admin group ls "${MINIO_ALIAS_NAME}"
        ;;
    info-group)
        [ "$#" -ne 1 ] && log_error "Usage: info-group <GROUPNAME>" && exit 1
        mc admin group info "${MINIO_ALIAS_NAME}" "$1"
        ;;
    add-user-to-group)
        [ "$#" -ne 2 ] && log_error "Usage: add-user-to-group <GROUPNAME> <USERNAME>" && exit 1
        mc admin group add "${MINIO_ALIAS_NAME}" "$1" "$2"
        ;;
    remove-user-from-group)
        [ "$#" -ne 2 ] && log_error "Usage: remove-user-from-group <GROUPNAME> <USERNAME>" && exit 1
        mc admin group rm "${MINIO_ALIAS_NAME}" "$1" "$2"
        ;;
    *)
        log_error "Invalid action: ${ACTION}"
        usage
        ;;
esac

log_info "Action '${ACTION}' completed successfully."