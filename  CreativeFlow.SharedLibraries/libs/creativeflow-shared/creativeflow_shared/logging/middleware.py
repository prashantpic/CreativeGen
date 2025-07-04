"""
Contains optional logging middleware for common Python web frameworks (e.g., FastAPI)
to automatically log request/response details and manage correlation IDs.

Requirement Mapping: DEP-005 (Standardized Log Format)
"""
import logging
import time
import uuid
from typing import Awaitable, Callable

from starlette.types import ASGIApp, Receive, Scope, Send

from ..core.constants import REQUEST_ID_HEADER
from .config import add_correlation_id

# Type alias for the wrapped send function
SendCallable = Callable[[dict], Awaitable[None]]


class FastAPILoggingMiddleware:
    """
    ASGI middleware for FastAPI to provide structured request/response logging
    and correlation ID management.
    """

    def __init__(self, app: ASGIApp, logger: logging.Logger):
        self.app = app
        self.logger = logger

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """
        The main middleware entry point for each request.
        """
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request_id = scope["headers"].get(REQUEST_ID_HEADER.lower().encode("utf-8"))
        if request_id:
            correlation_id = request_id.decode("utf-8")
        else:
            correlation_id = str(uuid.uuid4())

        # Set the correlation ID for the context of this request
        token = add_correlation_id(correlation_id)

        start_time = time.perf_counter()
        status_code = 500  # Default to 500 in case of an unhandled exception

        async def send_wrapper(message: dict) -> None:
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
            await send(message)

        try:
            self.logger.info(
                "Request started",
                extra={
                    "http.method": scope["method"],
                    "http.path": scope["path"],
                    "http.client_ip": scope.get("client", (None, None))[0],
                    "http.headers": {
                        k.decode(): v.decode() for k, v in scope["headers"]
                    },
                },
            )
            await self.app(scope, receive, send_wrapper)
        except Exception as e:
            self.logger.exception(f"Unhandled exception during request: {e}")
            # The exception will be propagated and handled by FastAPI's exception handlers
            raise
        finally:
            duration_ms = (time.perf_counter() - start_time) * 1000
            self.logger.info(
                "Request finished",
                extra={
                    "http.status_code": status_code,
                    "http.duration_ms": round(duration_ms, 2),
                },
            )
            # Reset the context variable to its previous state
            _correlation_id_var.reset(token)