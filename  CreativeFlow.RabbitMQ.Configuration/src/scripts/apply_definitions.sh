#!/bin/bash
#
# apply_definitions.sh
#
# This script applies the RabbitMQ topology and policies defined in a JSON file
# to a running RabbitMQ cluster via the Management HTTP API.
#
# It is designed to be idempotent. Running it multiple times will result in the
# same final state without causing errors.
#
# Dependencies: curl
#
# Configuration is sourced from environment variables, which can be set in
# `../config/rabbitmq_env.sh`.

set -euo pipefail

# Determine the script's directory to find other files relative to it
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
CONFIG_DIR="${SCRIPT_DIR}/../config"
DEFINITIONS_FILE="${SCRIPT_DIR}/../definitions.json"

# Source environment variables if the config file exists
if [ -f "${CONFIG_DIR}/rabbitmq_env.sh" ]; then
    # shellcheck source=../config/rabbitmq_env.sh.template
    source "${CONFIG_DIR}/rabbitmq_env.sh"
fi

# Set default values for environment variables if they are not already set
RABBITMQ_MANAGEMENT_URL="${RABBITMQ_MANAGEMENT_URL:-http://localhost:15672}"
RABBITMQ_ADMIN_USER="${RABBITMQ_ADMIN_USER:-guest}"
RABBITMQ_ADMIN_PASS="${RABBITMQ_ADMIN_PASS:-guest}"
RABBITMQ_DEFAULT_VHOST="${RABBITMQ_DEFAULT_VHOST:-/}"

# The vhost name in the URL must be URL-encoded. '/' becomes '%2f'.
VHOST_ENCODED=$(python -c "import urllib.parse; print(urllib.parse.quote_plus('${RABBITMQ_DEFAULT_VHOST}'))")

echo "--- RabbitMQ Configuration Applicator ---"
echo "Target URL:      ${RABBITMQ_MANAGEMENT_URL}"
echo "Admin User:      ${RABBITMQ_ADMIN_USER}"
echo "Target VHost:    ${RABBITMQ_DEFAULT_VHOST}"
echo "Definitions File: ${DEFINITIONS_FILE}"
echo "-----------------------------------------"

# Check if the definitions file exists and is readable
if [ ! -r "${DEFINITIONS_FILE}" ]; then
    echo "ERROR: Definitions file not found or not readable at ${DEFINITIONS_FILE}" >&2
    exit 1
fi

echo "Attempting to upload definitions..."

# Use curl to upload the definitions file.
# -s: silent mode
# -u: user:password for basic authentication
# -H: set content-type header
# -X: specify request method
# -w: write out the HTTP status code
# -o: redirect response body to /dev/null
# -d@: send data from a file
API_URL="${RABBITMQ_MANAGEMENT_URL}/api/definitions/${VHOST_ENCODED}"

HTTP_STATUS=$(curl -s -u "${RABBITMQ_ADMIN_USER}:${RABBITMQ_ADMIN_PASS}" \
    -H "content-type:application/json" \
    -X POST \
    -w "%{http_code}" \
    -o /dev/null \
    "${API_URL}" \
    -d @"${DEFINITIONS_FILE}")

# Check the HTTP response code for success
if [ "${HTTP_STATUS}" -eq 201 ] || [ "${HTTP_STATUS}" -eq 204 ]; then
    echo "SUCCESS: RabbitMQ definitions applied successfully. (HTTP Status: ${HTTP_STATUS})"
    exit 0
else
    echo "ERROR: Failed to apply RabbitMQ definitions." >&2
    echo "The management API at ${API_URL} returned HTTP status ${HTTP_STATUS}." >&2
    echo "Please check the RabbitMQ server logs and ensure credentials are correct." >&2
    exit 1
fi