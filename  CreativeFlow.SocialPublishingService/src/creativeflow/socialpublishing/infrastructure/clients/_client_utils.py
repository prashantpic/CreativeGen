"""
Utility functions for social media clients, e.g., retry logic,
specific error mapping.
"""
import asyncio
import functools
import logging
from typing import Any, Callable, Optional

import httpx

from ...application.exceptions import PlatformApiError, RateLimitError

logger = logging.getLogger(__name__)


def map_platform_error(
    platform_name: str, status_code: int, response_json: Optional[dict]
) -> PlatformApiError:
    """
    Maps a platform's HTTP error response to a standardized application exception.

    Args:
        platform_name: The name of the social media platform.
        status_code: The HTTP status code of the error response.
        response_json: The parsed JSON body of the error response.

    Returns:
        A PlatformApiError or RateLimitError instance.
    """
    details = response_json or {"error": "No response body"}
    if status_code == 429:
        return RateLimitError(
            platform=platform_name, status_code=status_code, details=details
        )
    return PlatformApiError(
        platform=platform_name, status_code=status_code, details=details
    )


def http_retry_decorator(
    max_retries: int = 3, delay_seconds: float = 1.0, backoff_factor: float = 2.0
) -> Callable:
    """
    A decorator for retrying HTTP requests with exponential backoff.

    Retries on httpx.TransportError (network issues) or 5xx server errors.

    Args:
        max_retries: The maximum number of retries.
        delay_seconds: The initial delay between retries.
        backoff_factor: The factor by which the delay increases for each retry.

    Returns:
        A decorator that can be applied to async methods making HTTP calls.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except (httpx.TransportError, httpx.HTTPStatusError) as e:
                    last_exception = e
                    if isinstance(e, httpx.HTTPStatusError):
                        # Retry only on 5xx server errors, not client errors (4xx)
                        if not (500 <= e.response.status_code < 600):
                            raise

                    if attempt < max_retries:
                        current_delay = delay_seconds * (backoff_factor**attempt)
                        logger.warning(
                            "HTTP request failed on attempt %d for function %s. Retrying in %.2f seconds. Error: %s",
                            attempt + 1,
                            func.__name__,
                            current_delay,
                            e,
                        )
                        await asyncio.sleep(current_delay)
                    else:
                        logger.error(
                            "HTTP request failed after %d retries for function %s. Giving up. Final Error: %s",
                            max_retries,
                            func.__name__,
                            e,
                        )
                        raise
            # This line should theoretically be unreachable
            raise last_exception  # type: ignore
        return wrapper
    return decorator