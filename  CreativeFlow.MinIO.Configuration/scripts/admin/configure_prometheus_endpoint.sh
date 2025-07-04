#!/bin/bash
#
# CreativeFlow.MinIO.Configuration - Prometheus Endpoint Configuration Generator
#
# Requirement Mapping: DEP-005
#
# This script generates the Prometheus scrape configuration needed to monitor
# a MinIO instance. It does not configure MinIO itself, but rather provides
# the necessary config block for your 'prometheus.yml' file.
#

set -e
set -o pipefail

# Source common utilities
source "$(dirname "$0")/../common_utils.sh"

# --- Main Script Logic ---

log_info "Starting Prometheus configuration generation..."

# Check for sourced environment and mc command
if [ -f "$(dirname "$0")/../../set_env.sh" ]; then
    source "$(dirname "$0")/../../set_env.sh"
fi
check_env_vars "MINIO_ALIAS_NAME"
check_mc_command

# Set JOB_NAME from the first argument, or default to 'minio-job'
JOB_NAME="${1:-minio-job}"

log_info "Generating Prometheus scrape configuration for job '${JOB_NAME}' on alias '${MINIO_ALIAS_NAME}'..."

log_info "--- Prometheus Configuration (add this to your prometheus.yml 'scrape_configs' section) ---"
# Execute the mc command to generate the config. The output is the YAML block.
mc admin prometheus generate "${MINIO_ALIAS_NAME}" "${JOB_NAME}"
log_info "-------------------------------------------------------------------------------------------"

log_info "Generation complete."
log_info "Ensure your Prometheus server has network access to the MinIO server's metrics endpoint."
log_info "If your MinIO metrics endpoint requires authentication, you may need to adjust the generated config."