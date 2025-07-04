# Stage 1: Builder
# Install dependencies into a virtual environment.
FROM python:3.12-slim as builder

# Set poetry environment variables
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Install poetry
RUN pip install poetry

# Copy project definition files
WORKDIR /app
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry install --no-dev --no-root

# Stage 2: Final Image
# Create a lean final image with the installed dependencies and application code.
FROM python:3.12-slim

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash appuser

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy virtual environment from the builder stage
COPY --from=builder /app/.venv /opt/venv
# Copy application source code
COPY src /app/src

# Activate the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Set ownership and working directory
RUN chown -R appuser:appuser /app /opt/venv
USER appuser
WORKDIR /app/src

# Expose the port the application will run on
EXPOSE 8000

# Set the command to run the application
CMD ["uvicorn", "creativeflow.service.notification.main:app", "--host", "0.0.0.0", "--port", "8000"]