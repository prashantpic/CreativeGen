#!/bin/bash
#
# check_cluster_status.sh: Displays RabbitMQ cluster status.
#
# This script is a simple wrapper around 'rabbitmqctl cluster_status'.
# It exits with the same status code as the underlying command, making it
# suitable for use in automated health checks and monitoring scripts.
#
# For more advanced automated checks, the output can be piped to tools like
# 'grep' to check for specific conditions, e.g., network partitions.
#
# Example: ./check_cluster_status.sh | grep "partitions,"
# If this command produces output, there is a network partition in the cluster.
#

set -eo pipefail

echo "Checking RabbitMQ cluster status..."
echo "---------------------------------"

# Execute the cluster_status command
rabbitmqctl cluster_status

# The script will exit with the status code of the last command run,
# which is rabbitmqctl in this case.
exit $?