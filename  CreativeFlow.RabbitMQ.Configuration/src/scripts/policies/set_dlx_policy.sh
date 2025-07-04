#!/bin/bash
#
# set_dlx_policy.sh
#
# This script applies a Dead Letter Exchange (DLX) policy to RabbitMQ queues
# using the rabbitmqctl command-line tool.
#
# This ensures that messages that are rejected or expire are routed to a
# specified exchange for later inspection or reprocessing.
#
# While this can be defined in definitions.json, this script is useful for
# dynamic or ad-hoc policy management.
#
# Dependencies: rabbitmqctl
#
# Usage:
# ./set_dlx_policy.sh <vhost> <policy_name> <queue_pattern> <dlx_name> [dlx_routing_key]
#
# Example:
# ./set_dlx_policy.sh "creativeflow_vhost" "dlx-ai-tasks" "^q\\.ai\\.generation\\.tasks$" "ex.dlx" "dlx.ai.generation"
# ./set_dlx_policy.sh "creativeflow_vhost" "dlx-common" "^q\\.notifications\\." "ex.dlx"

set -e

# --- Functions ---
usage() {
    echo "Usage: $0 <vhost> <policy_name> <queue_pattern> <dlx_name> [dlx_routing_key]"
    echo
    echo "Arguments:"
    echo "  vhost:            The virtual host to apply the policy to."
    echo "  policy_name:      A unique name for the policy (e.g., 'dlx-for-ai-queues')."
    echo "  queue_pattern:    A regex pattern to match queue names (e.g., '^q\\.ai\\..*')."
    echo "  dlx_name:         The name of the exchange to use as the dead-letter exchange."
    echo "  dlx_routing_key:  (Optional) The routing key to use when dead-lettering messages."
    echo
}

# --- Main Script ---
if [[ "$#" -lt 4 || "$#" -gt 5 ]]; then
    echo "Error: Incorrect number of arguments." >&2
    usage
    exit 1
fi

VHOST="$1"
POLICY_NAME="$2"
QUEUE_PATTERN="$3"
DLX_NAME="$4"
DLRK_NAME="${5:-}" # Optional 5th argument

# Construct the policy definition JSON string.
if [ -n "${DLRK_NAME}" ]; then
    DLX_DEFINITION_JSON="{\"dead-letter-exchange\":\"${DLX_NAME}\", \"dead-letter-routing-key\":\"${DLRK_NAME}\"}"
else
    DLX_DEFINITION_JSON="{\"dead-letter-exchange\":\"${DLX_NAME}\"}"
fi

echo "Applying DLX policy..."
echo "  VHost:         ${VHOST}"
echo "  Policy Name:   ${POLICY_NAME}"
echo "  Queue Pattern: ${QUEUE_PATTERN}"
echo "  Definition:    ${DLX_DEFINITION_JSON}"
echo

# Construct and execute the rabbitmqctl command
rabbitmqctl set_policy -p "${VHOST}" --apply-to queues "${POLICY_NAME}" "${QUEUE_PATTERN}" "${DLX_DEFINITION_JSON}"

echo "SUCCESS: Dead Letter Exchange policy '${POLICY_NAME}' was set successfully on vhost '${VHOST}'."