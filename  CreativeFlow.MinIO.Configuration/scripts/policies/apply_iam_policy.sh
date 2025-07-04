#!/bin/bash
#
# CreativeFlow.MinIO.Configuration - IAM Policy Application Script
#
# Requirement Mapping: SEC-006
#
# This script applies an IAM-like policy to a specified MinIO user or group.
# The policy can be a predefined MinIO policy name or a path to a JSON file.
#

set -e
set -o pipefail

# Source common utilities
source "$(dirname "$0")/../common_utils.sh"

# --- Functions ---
usage() {
    echo "Usage: $0 <user|group> <TARGET_NAME> <POLICY_NAME_OR_FILE_PATH>"
    echo ""
    echo "Applies an IAM policy to a MinIO user or group."
    echo ""
    echo "Arguments:"
    echo "  <user|group>             : The type of target to apply the policy to."
    echo "  <TARGET_NAME>            : The name of the user or group."
    echo "  <POLICY_NAME_OR_FILE_PATH> : The name of a predefined policy (e.g., readonly)"
    echo "                           or the path to a policy JSON file (e.g., ../config_templates/iam_policy_example.json)."
    echo ""
    echo "Example (using a file):"
    echo "  $0 group readonly-group ../config_templates/iam_policy_example.json"
    echo ""
    echo "Example (using a predefined policy):"
    echo "  $0 user testuser readonly"
    exit 1
}

# --- Main Script Logic ---

# Check for sourced environment and mc command
if [ -f "$(dirname "$0")/../../set_env.sh" ]; then
    source "$(dirname "$0")/../../set_env.sh"
fi
check_env_vars "MINIO_ALIAS_NAME"
check_mc_command

# Validate input arguments
if [ "$#" -ne 3 ]; then
    log_error "Invalid number of arguments."
    usage
fi

TARGET_TYPE="$1"
TARGET_NAME="$2"
POLICY_INPUT="$3"
POLICY_TO_APPLY=""

# Check if the policy input is a file
if [ -f "${POLICY_INPUT}" ]; then
    POLICY_FILE_PATH="${POLICY_INPUT}"
    # Derive policy name from the filename (e.g., /path/to/my-policy.json -> my-policy)
    POLICY_NAME=$(basename "${POLICY_FILE_PATH}" .json)
    log_info "Policy file provided. Will add/update policy named '${POLICY_NAME}' from file '${POLICY_FILE_PATH}'."
    
    # Add the policy to MinIO. This command will update the policy if it already exists.
    if mc admin policy add "${MINIO_ALIAS_NAME}" "${POLICY_NAME}" "${POLICY_FILE_PATH}"; then
        log_info "Policy '${POLICY_NAME}' created/updated on MinIO."
    else
        log_error "Failed to add policy '${POLICY_NAME}' from file. The file may be invalid or you lack permissions."
        exit 1
    fi
    POLICY_TO_APPLY="${POLICY_NAME}"
else
    log_info "Policy file not found at '${POLICY_INPUT}'. Assuming it is a predefined policy name."
    POLICY_TO_APPLY="${POLICY_INPUT}"
fi

# Apply the policy to the user or group
case "${TARGET_TYPE}" in
    user)
        log_info "Setting policy '${POLICY_TO_APPLY}' for user '${TARGET_NAME}'..."
        if mc admin policy set "${MINIO_ALIAS_NAME}" "${POLICY_TO_APPLY}" user="${TARGET_NAME}"; then
            log_info "Successfully set policy for user '${TARGET_NAME}'."
        else
            log_error "Failed to set policy for user '${TARGET_NAME}'. Check if user and policy exist."
            exit 1
        fi
        ;;
    group)
        log_info "Setting policy '${POLICY_TO_APPLY}' for group '${TARGET_NAME}'..."
        if mc admin policy set "${MINIO_ALIAS_NAME}" "${POLICY_TO_APPLY}" group="${TARGET_NAME}"; then
            log_info "Successfully set policy for group '${TARGET_NAME}'."
        else
            log_error "Failed to set policy for group '${TARGET_NAME}'. Check if group and policy exist."
            exit 1
        fi
        ;;
    *)
        log_error "Invalid target type '${TARGET_TYPE}'. Must be 'user' or 'group'."
        usage
        ;;
esac

log_info "IAM policy application completed."