#!/bin/bash
#
# CreativeFlow.MinIO.Configuration - Initial Bucket Policy Setter
#
# Requirement Mapping: Section 7.4.1, NFR-006
#
# This script applies initial default access policies to the core MinIO buckets.
# It uses simple canned policies ('private', 'download', etc.). For complex
# policies, use the 'apply_iam_policy.sh' script.
#

set -e
set -o pipefail

# Source common utilities
source "$(dirname "$0")/../common_utils.sh"

# --- Main Script Logic ---

log_info "Starting initial bucket policy application process..."

# Check for sourced environment and mc command
if [ -f "$(dirname "$0")/../../set_env.sh" ]; then
    source "$(dirname "$0")/../../set_env.sh"
fi
check_env_vars "MINIO_ALIAS_NAME"
check_mc_command

# Define the policies for each bucket.
# 'private': No anonymous access.
# 'download': Anonymous GET access.
# 'upload': Anonymous PUT access (use with caution).
# 'public': Anonymous GET and PUT access (use with extreme caution).
declare -A BUCKET_POLICIES
BUCKET_POLICIES["user-uploads"]="private"
BUCKET_POLICIES["generated-creatives"]="private"
BUCKET_POLICIES["brand-kits"]="private"
BUCKET_POLICIES["templates"]="download"
BUCKET_POLICIES["system-assets"]="download"
BUCKET_POLICIES["model-artifacts"]="private"
BUCKET_POLICIES["database-backups"]="private"
BUCKET_POLICIES["logs-archive"]="private"

# Loop through the associative array and set policies
for bucket_name in "${!BUCKET_POLICIES[@]}"; do
    policy_type="${BUCKET_POLICIES[$bucket_name]}"
    log_info "Setting policy '${policy_type}' for bucket '${MINIO_ALIAS_NAME}/${bucket_name}'..."
    
    if mc policy set "${policy_type}" "${MINIO_ALIAS_NAME}/${bucket_name}"; then
        log_info "Successfully set policy for '${MINIO_ALIAS_NAME}/${bucket_name}' to '${policy_type}'."
    else
        log_error "Failed to set policy for '${MINIO_ALIAS_NAME}/${bucket_name}'. Please check bucket existence and your permissions."
        exit 1
    fi
done

log_info "Initial bucket policy application completed."