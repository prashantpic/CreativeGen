#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Wait for the database to be ready (optional, but good practice)
# This requires netcat (nc) to be installed in the Docker image
# You might need to add `apt-get update && apt-get install -y netcat-openbsd` to the Dockerfile
# while ! nc -z ${DB_HOST:-postgres} ${DB_PORT:-5432}; do
#   echo "Waiting for PostgreSQL..."
#   sleep 1
# done
# echo "PostgreSQL started"

# Run database migrations
echo "Running Alembic migrations..."
alembic -c src/creativeflow/mlops_service/alembic.ini upgrade head
echo "Migrations complete."

# Start the application
# The command to run is passed as arguments to this script ("$@")
# This allows overriding the default CMD in the Dockerfile, e.g., for running tests
echo "Starting MLOps Service..."
exec "$@"