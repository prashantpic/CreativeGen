ARG PYTHON_VERSION=3.12.2-slim
FROM python:${PYTHON_VERSION}

LABEL maintainer="CreativeFlow AI Team <devops@creativeflow.ai>"
LABEL description="Base image for custom Python AI models served with FastAPI on CreativeFlow AI."

# Ensures that Python outputs are sent straight to terminal without being first buffered,
# and that Python doesn't try to write .pyc files to the container.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy base requirements and install them. Using a distinct name for the base requirements
# file allows model-specific Dockerfiles to add their own `requirements.txt` without conflict.
COPY ./runtime-bases/custom-python-fastapi/requirements.txt /app/requirements_base.txt
RUN pip install --no-cache-dir -r requirements_base.txt

# Copy the base application structure.
# Specific model images can add their own `src/` and override/extend this base.
COPY ./runtime-bases/custom-python-fastapi/src /app/src

# Expose the port the app runs on
EXPOSE 8000

# Default command to run the FastAPI application using Uvicorn.
# This assumes the main FastAPI app instance is named `app` in `src/main.py`.
# For GPU-bound tasks, 1 worker is typical. For IO-bound tasks, this could be increased.
# The number of workers can also be configured via K8s deployment arguments.
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]