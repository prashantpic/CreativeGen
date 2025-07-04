#!/bin/bash
#
# set_ha_policy.sh
#
# This script applies a High Availability (HA) policy to RabbitMQ queues
# using the rabbitmqctl command-line tool.
#
# This is useful for ensuring messages are replicated across cluster nodes
# for fault tolerance, especially for classic mirrored queues. For modern
# setups, using Quorum Queues is often preferred and can be defined
# directly in definitions.json.
#
# Dependencies: rabbitmqctl
#
# Usage:
# ./set_ha_policy.sh <vhost> <policy_name> <queue_pattern> <ha_definition_json>
#
# Example:
# ./set_ha_policy.sh "creativeflow_vhost" "ha-all" "^q\.critical\." '{"ha-mode":"all","ha-sync-mode":"automatic"}'
# ./set_ha_policy.sh "creativeflow_vhost" "ha-exactly-2" "^q\.replicated\." '{"ha-mode":"exactly","ha-params":2,"ha-sync-mode":"automatic"}'

set -e

# --- Functions ---
usage() {
    echo "Usage: $0 <vhost> <policy_name> <queue_pattern> <ha_definition_json>"
    echo
    echo "Arguments:"
    echo "  vhost:                The virtual host to apply the policy to."
    echo "  policy_name:          A unique name for the policy (e.g., 'ha-critical-queues')."
    echo "  queue_pattern:        A regex pattern to match queue names (e.g., '^q\\.ai\\..*')."
    echo "  ha_definition_json:   The HA policy definition in JSON format."
    echo "                        Example: '{\"ha-mode\":\"all\", \"ha-sync-mode\":\"automatic\"}'"
    echo "                        Example: '{\"ha-mode\":\"exactly\", \"ha-params\":2, \"ha-sync-mode\":\"automatic\"}'"
    echo
}

# --- Main Script ---
if [ "$#" -ne 4 ]; then
    echo "Error: Incorrect number of arguments." >&2
    usage
    exit 1
fi

VHOST="$1"
POLICY_NAME="$2"
QUEUE_PATTERN="$3"
HA_DEFINITION_JSON="$4"

echo "Applying HA policy..."
echo "  VHost:         ${VHOST}"
echo "  Policy Name:   ${POLICY_NAME}"
echo "  Queue Pattern: ${QUEUE_PATTERN}"
echo "  Definition:    ${HA_DEFINITION_JSON}"
echo

# Construct and execute the rabbitmqctl command
# The --apply-to "queues" is important to specify the entity type.
rabbitmqctl set_policy -p "${VHOST}" --apply-to queues "${POLICY_NAME}" "${QUEUE_PATTERN}" "${HA_DEFINITION_JSON}"

echo "SUCCESS: High Availability policy '${POLICY_NAME}' was set successfully on vhost '${VHOST}'."