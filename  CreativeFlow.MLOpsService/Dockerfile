# --- Build Stage ---
FROM python:3.10-slim as builder

# Set working directory
WORKDIR /app

# Install poetry
RUN pip install poetry==1.8.2

# Copy only dependency-defining files to leverage Docker cache
COPY pyproject.toml poetry.lock ./

# Install dependencies, --no-root avoids installing the project itself
# --only main installs only production dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root --only main

# --- Final Stage ---
FROM python:3.10-slim as final

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Copy installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy the application source code
COPY src/ /app/src/
COPY alembic.ini /app/
COPY src/creativeflow/mlops_service/alembic /app/src/creativeflow/mlops_service/alembic
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose the port the app runs on
EXPOSE 8000

# Set the entrypoint for the container
ENTRYPOINT ["/app/entrypoint.sh"]