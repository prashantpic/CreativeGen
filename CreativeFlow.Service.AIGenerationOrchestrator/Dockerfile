# Stage 1: Builder - Install dependencies
FROM python:3.11-slim as builder

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy project dependency files
COPY pyproject.toml poetry.lock ./

# Install only production dependencies
RUN poetry install --no-dev --no-root

# Stage 2: Final - Create the runtime image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv ./.venv

# Activate the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Copy the application source code
COPY ./src ./src

# Expose the port the application will run on
EXPOSE 8000

# Command to run the application
# The entry point is src/creativeflow/service/aigeneration_orchestrator/main.py
# The FastAPI app instance is named 'app'
CMD ["uvicorn", "src.creativeflow.service.aigeneration_orchestrator.main:app", "--host", "0.0.0.0", "--port", "8000"]