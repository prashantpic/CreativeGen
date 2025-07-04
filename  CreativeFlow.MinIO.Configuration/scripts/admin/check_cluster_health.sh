#!/bin/bash
#
# CreativeFlow.MinIO.Configuration - Cluster Health Check Script
#
# Requirement Mapping: DEP-001
#
# This script runs basic health and status checks on the MinIO cluster
# using 'mc admin' commands.
#

set -e
set -o pipefail

# Source common utilities
source "$(dirname "$0")/../common_utils.sh"

# --- Main Script Logic ---

log_info "Starting MinIO cluster health check..."

# Check for sourced environment and mc command
if [ -f "$(dirname "$0")/../../set_env.sh" ]; then
    source "$(dirname "$0")/../../set_env.sh"
fi
check_env_vars "MINIO_ALIAS_NAME"
check_mc_command

log_info "--- Fetching MinIO cluster information for alias '${MINIO_ALIAS_NAME}' ---"
mc admin info "${MINIO_ALIAS_NAME}"
echo "" # Add a blank line for readability

log_info "--- Checking for any healing activity ---"
log_info "This command shows the status of self-healing scans on drives and objects."
mc admin heal "${MINIO_ALIAS_NAME}"
echo "" # Add a blank line for readability

log_info "Cluster health check completed."