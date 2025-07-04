# Stage 1: Builder
# Use a specific Python version for reproducibility
FROM python:3.11-slim as builder

# Set the working directory
WORKDIR /app

# Install poetry or just use pip
# Using pip for simplicity here
COPY requirements.txt .
# Install production dependencies
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt


# Stage 2: Final Image
# Use the same Python version
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy installed wheels from the builder stage
COPY --from=builder /app/wheels /wheels
# Install the dependencies from the wheels
RUN pip install --no-cache /wheels/*

# Copy the entrypoint script and make it executable
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Copy the application source code
COPY src/creativeflow/mlops_service ./src/creativeflow/mlops_service

# Expose the port the app runs on
EXPOSE 8000

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command can be overridden
# The entrypoint script will run this
CMD ["uvicorn", "src.creativeflow.mlops_service.main:app", "--host", "0.0.0.0", "--port", "8000"]