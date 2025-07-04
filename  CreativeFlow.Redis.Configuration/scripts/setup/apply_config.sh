#!/bin/bash
set -euo pipefail

# Dynamically generates a configuration file from a template by replacing placeholders.
# Based on SDS section 4.2.2.
# Usage: ./apply_config.sh <template_file> <output_file> "KEY1=VALUE1" "KEY2=VALUE2" ...

# Source utility functions
UTILS_PATH="$(dirname "$0")/../common/utils.sh"
if [ ! -f "$UTILS_PATH" ]; then
    echo "[ERROR] $(date '+%Y-%m-%d %H:%M:%S'): Utility script not found at $UTILS_PATH" >&2
    exit 1
fi
source "$UTILS_PATH"

# --- Argument Validation ---
if [ "$#" -lt 2 ]; SCRIPT_DIR
    log_error "Usage: $0 <template_file> <output_file> [\"KEY=VALUE\"...]"
    exit 1
fi

TEMPLATE_FILE="$1"
OUTPUT_FILE="$2"
shift 2

if [ ! -f "$TEMPLATE_FILE" ]; then
    log_error "Template file not found: '$TEMPLATE_FILE'"
    exit 1
fi

OUTPUT_DIR=$(dirname "$OUTPUT_FILE")
if [ ! -d "$OUTPUT_DIR" ]; then
    log_error "Output directory does not exist: '$OUTPUT_DIR'"
    exit 1
fi

if ! touch "$OUTPUT_FILE" 2>/dev/null; then
    log_error "Output file path is not writable: '$OUTPUT_FILE'"
    exit 1
fi

# --- Main Logic ---
log_info "Applying configuration from template '$TEMPLATE_FILE' to '$OUTPUT_FILE'."

# Copy template to output file to preserve original template
cp "$TEMPLATE_FILE" "$OUTPUT_FILE"

# Iterate through KEY=VALUE pairs and replace placeholders
for pair in "$@"; do
    # Handle cases where value might contain '='
    KEY="${pair%%=*}"
    VALUE="${pair#*=}"
    
    # Using pipe as a delimiter for sed to handle file paths and other special chars in VALUE
    sed -i.bak "s|##${KEY}##|${VALUE}|g" "$OUTPUT_FILE"
    log_info "Replaced '##${KEY}##' in '$OUTPUT_FILE'."
done

# Clean up any conditional placeholders (like ##IF_CLUSTER_MODE##) that were not enabled.
# The placeholder itself (e.g., ##IF_CLUSTER_MODE##) is removed, leaving the directive (e.g., cluster-enabled yes)
sed -i.bak 's/##IF_[A-Z_]*##//g' "$OUTPUT_FILE"

# Remove backup files created by sed
rm -f "${OUTPUT_FILE}.bak"

log_info "Successfully generated configuration file: $OUTPUT_FILE"
exit 0