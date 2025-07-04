#!/bin/bash
#
# CreativeFlow.MinIO.Configuration - Bucket Disaster Recovery Replication Setup
#
# Requirement Mapping: NFR-004, CPIO-005, REQ-DA-012
#
# This script configures asynchronous bucket replication to a Disaster Recovery (DR) site.
# It assumes the DR MinIO instance has already been configured as an alias in `mc`.
#

set -e
set -o pipefail

# Source common utilities
source "$(dirname "$0")/../common_utils.sh"

# --- Functions ---

usage() {
    echo "Usage: $0 <SOURCE_BUCKET_PATH> <DR_TARGET_ALIAS> <DR_TARGET_BUCKET_NAME> <REPLICATION_RULE_NAME>"
    echo ""
    echo "Configures asynchronous bucket replication to a DR site."
    echo ""
    echo "Arguments:"
    echo "  SOURCE_BUCKET_PATH     : Full path to the source bucket (e.g., myminio/user-uploads)."
    echo "  DR_TARGET_ALIAS        : The 'mc' alias for the DR MinIO instance (must be pre-configured)."
    echo "  DR_TARGET_BUCKET_NAME  : The name of the bucket on the DR instance."
    echo "  REPLICATION_RULE_NAME  : A unique name for the replication rule (e.g., 'dr-replication-rule-1')."
    echo ""
    echo "Example:"
    echo "  $0 myminio/database-backups minio-dr database-backups-dr dr-backups-rule"
    exit 1
}

# --- Main Script Logic ---

# Check for sourced environment and mc command
if [ -f "$(dirname "$0")/../../set_env.sh" ]; then
    source "$(dirname "$0")/../../set_env.sh"
fi
check_mc_command

# Validate input arguments
if [ "$#" -ne 4 ]; then
    log_error "Invalid number of arguments."
    usage
fi

SOURCE_BUCKET_PATH="$1"
DR_TARGET_ALIAS="$2"
DR_TARGET_BUCKET_NAME="$3"
REPLICATION_RULE_NAME="$4"

log_info "Starting bucket DR replication setup..."
log_info "  Source: ${SOURCE_BUCKET_PATH}"
log_info "  DR Target: ${DR_TARGET_ALIAS}/${DR_TARGET_BUCKET_NAME}"
log_info "  Rule Name: ${REPLICATION_RULE_NAME}"

# Ensure DR target bucket exists or create it
log_info "Checking for existence of DR target bucket '${DR_TARGET_ALIAS}/${DR_TARGET_BUCKET_NAME}'..."
if mc stat "${DR_TARGET_ALIAS}/${DR_TARGET_BUCKET_NAME}" &>/dev/null; then
    log_info "DR target bucket already exists."
else
    log_info "DR target bucket not found. Creating it..."
    if mc mb "${DR_TARGET_ALIAS}/${DR_TARGET_BUCKET_NAME}"; then
        log_info "DR target bucket created successfully."
    else
        log_error "Failed to create DR target bucket '${DR_TARGET_ALIAS}/${DR_TARGET_BUCKET_NAME}'. Check permissions on DR alias."
        exit 1
    fi
fi

# Add replication rule
# The --arn flag here refers to the pre-configured target alias.
# You can add more flags like --replicate "delete,existing-objects"
log_info "Adding replication rule..."
if mc replicate add "${SOURCE_BUCKET_PATH}" \
    --remote-bucket "arn:aws:s3:::${DR_TARGET_BUCKET_NAME}" \
    --arn "${DR_TARGET_ALIAS}" \
    --rule-name "${REPLICATION_RULE_NAME}" \
    --replicate "existing-objects,delete,delete-marker" \
    --priority 1; then
    log_info "Replication rule '${REPLICATION_RULE_NAME}' added successfully."
else
    log_error "Failed to add replication rule. Ensure versioning is enabled on the source bucket and permissions are correct."
    exit 1
fi

log_info "Verifying replication configuration..."
mc replicate ls "${SOURCE_BUCKET_PATH}"

log_info "Checking replication status (may take time to update)..."
mc replicate status "${SOURCE_BUCKET_PATH}" --rule-name "${REPLICATION_RULE_NAME}"

log_info "Bucket replication setup for '${SOURCE_BUCKET_PATH}' to DR site completed."