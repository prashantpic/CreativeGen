#!/bin/bash
#
# CreativeFlow.MinIO.Configuration - Initial Bucket Creation Script
#
# Requirement Mapping: Section 7.4.1
#
# This script creates the initial set of buckets required by the CreativeFlow AI platform.
# It is designed to be idempotent; it will not fail if a bucket already exists.
#

set -e
set -o pipefail

# Source common utilities
source "$(dirname "$0")/../common_utils.sh"

# --- Main Script Logic ---

log_info "Starting initial bucket creation process..."

# Check for sourced environment and mc command
if [ -f "$(dirname "$0")/../../set_env.sh" ]; then
    source "$(dirname "$0")/../../set_env.sh"
fi
check_env_vars "MINIO_ALIAS_NAME"
check_mc_command

# Define the list of buckets to be created as per SRS 7.4.1
BUCKETS=(
    "user-uploads"
    "generated-creatives"
    "brand-kits"
    "templates"
    "system-assets"
    "model-artifacts"
    "database-backups"
    "logs-archive"
)

# Loop through the BUCKETS array and create each one if it doesn't exist
for bucket_name in "${BUCKETS[@]}"; do
    log_info "Checking if bucket '${MINIO_ALIAS_NAME}/${bucket_name}' exists..."
    if mc stat "${MINIO_ALIAS_NAME}/${bucket_name}" &>/dev/null; then
        log_info "Bucket '${MINIO_ALIAS_NAME}/${bucket_name}' already exists. Skipping creation."
    else
        log_info "Creating bucket '${MINIO_ALIAS_NAME}/${bucket_name}'..."
        if mc mb "${MINIO_ALIAS_NAME}/${bucket_name}"; then
            log_info "Bucket '${MINIO_ALIAS_NAME}/${bucket_name}' created successfully."
        else
            log_error "Failed to create bucket '${MINIO_ALIAS_NAME}/${bucket_name}'. Exiting."
            exit 1
        fi
    fi
done

log_info "Bucket creation process completed successfully."