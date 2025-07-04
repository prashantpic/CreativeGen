"""
Contains common, reusable decorators for cross-cutting concerns.
"""
import functools
import logging
import time
from typing import Any, Callable, Optional


def timed(logger: Optional[logging.Logger] = None) -> Callable:
    """
    Decorator factory that logs the execution time of the wrapped function.

    Args:
        logger: An optional logger instance. If not provided, a logger is
                obtained using the function's module name.

    Returns:
        A decorator that can be applied to a function.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            log_target = logger if logger else logging.getLogger(func.__module__)
            start_time = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                end_time = time.perf_counter()
                elapsed_time_ms = (end_time - start_time) * 1000
                log_target.debug(
                    "Function '%s' executed in %.4f ms", func.__name__, elapsed_time_ms
                )

        return wrapper

    return decorator


def memoize(maxsize: int = 128, typed: bool = False) -> Callable:
    """
    Simple memoization decorator using Python's built-in LRU cache.

    Args:
        maxsize: The maximum number of recent calls to cache.
        typed: If True, arguments of different types will be cached separately.
               For example, f(3) and f(3.0) will be treated as distinct calls.

    Returns:
        A decorator that applies `functools.lru_cache`.
    """

    def decorator(func: Callable) -> Callable:
        return functools.lru_cache(maxsize=maxsize, typed=typed)(func)

    return decorator