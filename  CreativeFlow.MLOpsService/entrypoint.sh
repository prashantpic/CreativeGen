#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Run database migrations before starting the application.
# This ensures the database schema is up-to-date.
echo "Running Alembic migrations..."
alembic upgrade head
echo "Migrations complete."

# Start the MLOps Service using Uvicorn.
# The host and port are configurable via environment variables,
# with sensible defaults.
echo "Starting MLOps Service..."
exec uvicorn creativeflow.mlops_service.main:app \
    --host "${SERVICE_HOST:-0.0.0.0}" \
    --port "${SERVICE_PORT:-8000}" \
    --workers "${UVICORN_WORKERS:-1}" \
    --log-config src/creativeflow/mlops_service/utils/uvicorn_logging.json