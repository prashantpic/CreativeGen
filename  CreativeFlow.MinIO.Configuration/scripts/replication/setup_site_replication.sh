#!/bin/bash
#
# CreativeFlow.MinIO.Configuration - Site Replication Setup Script
#
# Requirement Mapping: NFR-004, CPIO-005, REQ-DA-012
#
# This script configures active-active multi-site replication from a primary
# site to a replica site.
#
# NOTE: This script configures ONE-WAY replication. For full active-active,
# you must run this script on the replica site, pointing back to the primary.
#

set -e
set -o pipefail

# Source common utilities
source "$(dirname "$0")/../common_utils.sh"

# --- Main Script Logic ---

log_info "Starting MinIO site replication setup..."

# Check for sourced environment and mc command
if [ -f "$(dirname "$0")/../../set_env.sh" ]; then
    source "$(dirname "$0")/../../set_env.sh"
fi
check_mc_command

# Check for required environment variables for replication
check_env_vars "PRIMARY_MINIO_ALIAS" "REPLICA_SITE_NAME" "REPLICA_ENDPOINT_URL" "REPLICA_ACCESS_KEY" "REPLICA_SECRET_KEY"

log_info "Configuring site replication from '${PRIMARY_MINIO_ALIAS}' to target site '${REPLICA_SITE_NAME}'..."

# Construct flags. Add more flags here as needed.
# e.g., --replicate existing-objects, --health-check-secs 30
REPLICATION_FLAGS="--priority 1"

# Configure the remote site target on the primary alias
if mc admin replicate add "${PRIMARY_MINIO_ALIAS}" "${REPLICA_SITE_NAME}" \
    --endpoint "${REPLICA_ENDPOINT_URL}" \
    --access-key "${REPLICA_ACCESS_KEY}" \
    --secret-key "${REPLICA_SECRET_KEY}" \
    ${REPLICATION_FLAGS}; then
    log_info "Successfully added replica site configuration."
else
    log_error "Failed to add replica site configuration. Please check credentials and network connectivity."
    log_error "Note: If the remote already exists, you may need to remove it first with 'mc admin replicate rm'."
    exit 1
fi

log_info "Verifying replication setup..."
mc admin replicate info "${PRIMARY_MINIO_ALIAS}" "${REPLICA_SITE_NAME}"

log_info "Site replication setup from '${PRIMARY_MINIO_ALIAS}' to '${REPLICA_SITE_NAME}' completed."
log_info "IMPORTANT: For full active-active replication, you must now run this script on the replica site, pointing back to this primary site."