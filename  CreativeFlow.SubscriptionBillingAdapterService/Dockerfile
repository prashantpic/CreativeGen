# Stage 1: Build the application dependencies
FROM python:3.11-slim as builder

WORKDIR /app

# Set environment variables to prevent Poetry from creating a virtualenv
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Install Poetry
RUN pip install poetry==1.8.2

# Copy only the files necessary for dependency installation
COPY pyproject.toml poetry.lock* ./

# Install dependencies, excluding development ones
RUN poetry install --no-root --no-dev

# Stage 2: Create the final production image
FROM python:3.11-slim

WORKDIR /app

# Create a non-root user for security
RUN groupadd -r appuser && useradd --no-log-init -r -g appuser appuser

# Copy installed dependencies from the builder stage
COPY --from=builder /app /app

# Copy application source code
COPY ./src ./src
COPY ./gunicorn_conf.py .

# Ensure correct ownership of the application files
RUN chown -R appuser:appuser /app

USER appuser

ENV PYTHONPATH=/app

EXPOSE 8000

# Command to run the application using Gunicorn for production
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-c", "./gunicorn_conf.py", "src.creativeflow.services.subbilling.main:app"]