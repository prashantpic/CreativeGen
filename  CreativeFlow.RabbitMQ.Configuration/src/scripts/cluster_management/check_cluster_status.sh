#!/bin/bash
#
# check_cluster_status.sh
#
# Provides a quick way to check the overall health and status of the RabbitMQ
# cluster using `rabbitmqctl`.
#
# It specifically checks for network partitions, which are a common and critical
# failure mode in RabbitMQ clusters.
#
# A healthy cluster should report an empty list of partitions: `partitions,[]`
#
# Exit Codes:
#   0: Cluster is healthy.
#   1: Cluster is unhealthy (command failed or partition detected).
#
# Dependencies: rabbitmqctl

set -uo pipefail

# Temporary file to store the output of rabbitmqctl
STATUS_FILE=$(mktemp)
# Ensure the temporary file is cleaned up on script exit
trap 'rm -f -- "$STATUS_FILE"' EXIT

echo "Checking RabbitMQ cluster status..."

# Execute rabbitmqctl and capture its output and exit code
if ! rabbitmqctl cluster_status > "$STATUS_FILE" 2>&1; then
    echo "Cluster is UNHEALTHY (rabbitmqctl command failed with exit code $?)." >&2
    echo "--- rabbitmqctl output ---" >&2
    cat "$STATUS_FILE" >&2
    echo "--------------------------" >&2
    exit 1
fi

# Check for the absence of network partitions in the output.
# grep -q is silent and returns exit code 0 if a match is found, 1 otherwise.
if grep -q 'partitions,\[\]' "$STATUS_FILE"; then
    echo "Cluster is HEALTHY (No partitions detected)."
    exit 0
else
    echo "Cluster is UNHEALTHY (Network partition detected or status is malformed!)." >&2
    echo "--- rabbitmqctl output ---" >&2
    cat "$STATUS_FILE" >&2
    echo "--------------------------" >&2
    exit 1
fi