# gunicorn_conf.py
# Configuration file for Gunicorn, used in the Docker container for production.

import multiprocessing
import os

# Server socket
# Bind to 0.0.0.0 to accept connections from any IP, essential for Docker.
bind = "0.0.0.0:8000"

# Worker processes
# A common formula is (2 * number of CPUs) + 1.
workers = multiprocessing.cpu_count() * 2 + 1

# Worker class for running FastAPI with Uvicorn
# This allows Gunicorn to manage the Uvicorn workers.
worker_class = "uvicorn.workers.UvicornWorker"

# Logging
# Log to stdout/stderr so that Docker/Kubernetes can capture and manage logs.
loglevel = os.getenv("LOG_LEVEL", "info").lower()
accesslog = "-"  # STDOUT
errorlog = "-"   # STDERR

# Worker timeout
# If a worker is silent for more than this number of seconds, it is killed and restarted.
# May need to be increased if some Odoo calls are expected to be very long.
timeout = int(os.getenv("GUNICORN_TIMEOUT", 120))

# Keep-Alive
# The number of seconds to wait for requests on a Keep-Alive connection.
keepalive = int(os.getenv("GUNICORN_KEEPALIVE", 5))

# Optional: Preload the application before forking workers
# This can save some memory, but may not be suitable if your app
# creates resources (like DB connections) that can't be shared across processes.
# preload_app = True