#!/bin/bash
#
# CreativeFlow.MinIO.Configuration - Bucket Lifecycle Policy Setter
#
# Requirement Mapping: Section 7.5
#
# This script configures a bucket lifecycle policy (ILM) using an XML
# configuration file.
#

set -e
set -o pipefail

# Source common utilities
source "$(dirname "$0")/../common_utils.sh"

# --- Functions ---
usage() {
    echo "Usage: $0 <BUCKET_NAME> <LIFECYCLE_POLICY_FILE_PATH>"
    echo ""
    echo "Applies a lifecycle (ILM) policy from an XML file to a bucket."
    echo ""
    echo "Arguments:"
    echo "  <BUCKET_NAME>                 : The name of the target bucket."
    echo "  <LIFECYCLE_POLICY_FILE_PATH>  : The path to the lifecycle policy XML file."
    echo ""
    echo "Example:"
    echo "  $0 logs-archive ../config_templates/lifecycle_policy_example.xml"
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
if [ "$#" -ne 2 ]; then
    log_error "Invalid number of arguments."
    usage
fi

BUCKET_NAME="$1"
LIFECYCLE_POLICY_FILE_PATH="$2"
FULL_BUCKET_PATH="${MINIO_ALIAS_NAME}/${BUCKET_NAME}"

if [ ! -f "${LIFECYCLE_POLICY_FILE_PATH}" ]; then
    log_error "Lifecycle policy file not found at: ${LIFECYCLE_POLICY_FILE_PATH}"
    exit 1
fi

log_info "Setting lifecycle policy from '${LIFECYCLE_POLICY_FILE_PATH}' for bucket '${FULL_BUCKET_PATH}'..."

if mc ilm set "${FULL_BUCKET_PATH}" "${LIFECYCLE_POLICY_FILE_PATH}"; then
    log_info "Lifecycle policy applied successfully to '${FULL_BUCKET_PATH}'."
    log_info "--- Current Lifecycle Configuration ---"
    mc ilm ls "${FULL_BUCKET_PATH}"
    log_info "---------------------------------------"
else
    log_error "Failed to apply lifecycle policy to '${FULL_BUCKET_PATH}'."
    log_error "Please ensure the bucket exists, versioning is enabled (if required by the policy), and the XML file is valid."
    exit 1
fi

log_info "Bucket lifecycle policy configuration completed."