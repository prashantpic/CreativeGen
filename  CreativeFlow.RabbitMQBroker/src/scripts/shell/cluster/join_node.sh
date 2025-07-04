#!/bin/bash
#
# join_node.sh: Automates adding a RabbitMQ node to an existing cluster.
#
# This script performs the necessary sequence of rabbitmqctl commands to
# securely join a cluster. It includes error checking at each step.
#
# WARNING: This script calls 'rabbitmqctl reset', which erases all data from
# the node being joined. It should only be run on a new or decommissioned node.
#

set -eo pipefail

# --- Functions ---
log_info() {
    echo "[INFO] $1"
}

log_error() {
    echo "[ERROR] $1" >&2
}

# --- Script Main ---

# Check for correct number of arguments
if [ "$#" -ne 1 ]; then
    log_error "Usage: $0 <master_node_name>"
    log_error "Example: $0 rabbit@node1_hostname"
    exit 1
fi

MASTER_NODE=$1
log_info "Attempting to join cluster with master node: ${MASTER_NODE}"

# Step 1: Stop the RabbitMQ application
log_info "Step 1: Stopping RabbitMQ application..."
rabbitmqctl stop_app
if [ $? -ne 0 ]; then
    log_error "Failed to stop the RabbitMQ application. Aborting."
    exit 1
fi
log_info "RabbitMQ application stopped successfully."

# Step 2: Reset the node state
# This is a destructive operation that clears all data on the current node.
log_info "Step 2: Resetting node state (clears all local data)..."
rabbitmqctl reset
if [ $? -ne 0 ]; then
    log_error "Failed to reset the node. Aborting."
    # Attempt to start the app again to leave it in a running state
    rabbitmqctl start_app
    exit 1
fi
log_info "Node reset successfully."

# Step 3: Join the cluster
log_info "Step 3: Joining cluster with master node '${MASTER_NODE}'..."
# Consider adding '--ram' flag if this node should be a RAM node:
# rabbitmqctl join_cluster "${MASTER_NODE}" --ram
rabbitmqctl join_cluster "${MASTER_NODE}"
if [ $? -ne 0 ]; then
    log_error "Failed to join the cluster. Aborting."
    # Attempt to start the app again to leave it in a running state
    rabbitmqctl start_app
    exit 1
fi
log_info "Successfully joined the cluster."

# Step 4: Start the RabbitMQ application on the newly joined node
log_info "Step 4: Starting RabbitMQ application..."
rabbitmqctl start_app
if [ $? -ne 0 ]; then
    log_error "Failed to start the RabbitMQ application after joining the cluster."
    exit 1
fi
log_info "RabbitMQ application started successfully."

echo
log_info "Node has successfully joined the cluster. Verify with 'check_cluster_status.sh'."
exit 0