from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os
from prometheus_client import Counter, Histogram, make_asgi_app # For metrics

# from .routers import predict # Example: if base has a generic predict router
# from .dependencies import load_model_globally # Example

# --- Prometheus Metrics Definition ---
# These metrics will be exposed on the /metrics endpoint.
REQUEST_COUNT = Counter(
    "custom_server_requests_total",
    "Total count of requests.",
    ["method", "endpoint", "http_status"]
)
REQUEST_LATENCY = Histogram(
    "custom_server_request_latency_seconds",
    "Histogram of request latencies.",
    ["method", "endpoint"]
)

# --- FastAPI App Initialization ---
app = FastAPI(
    title="CreativeFlow Custom AI Model Server - Base",
    description="Base FastAPI application for serving custom AI models. Specific models will extend this.",
    version="0.1.0"
)

# Mount the Prometheus ASGI app on the /metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# --- Application Events ---
# Example: Global model loading at startup (can be specialized by model image)
# This is typically handled within a model-specific handler to keep the base generic.
# model = None
# @app.on_event("startup")
# async def startup_event():
#     global model
#     model_path = os.getenv("MODEL_PATH")
#     if model_path:
#         # model = load_model_globally(model_path) # From dependencies.py
#         # print(f"Model loaded from {model_path}")
#     print("Base FastAPI application startup complete.")


# --- API Endpoints ---
@app.get("/health", summary="Health Check", tags=["System"])
async def health_check():
    """
    Performs a health check of the application.
    Returns HTTP 200 with a 'healthy' status if the application is running.
    This endpoint is used for Kubernetes liveness and readiness probes.
    """
    REQUEST_COUNT.labels(method="GET", endpoint="/health", http_status=200).inc()
    return JSONResponse(content={"status": "healthy"})

# --- Router Inclusion ---
# Specific models are expected to define their own routers for prediction endpoints
# and include them in their specialized main.py or by extending this base.
# Example:
# from .routers import specific_model_router
# app.include_router(specific_model_router, prefix="/v1/models/my-model", tags=["My Model"])