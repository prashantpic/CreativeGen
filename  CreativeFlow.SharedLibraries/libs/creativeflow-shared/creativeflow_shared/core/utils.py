"""
General-purpose utility functions shared across different services.
"""
import copy
import datetime
import uuid
from typing import Any


def generate_unique_id(prefix: str | None = None) -> str:
    """
    Generates a UUID v4 string.

    If a prefix is provided, it prepends it to the UUID string, separated by an underscore.
    e.g., "user_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

    Args:
        prefix: An optional string to prepend to the UUID.

    Returns:
        A unique identifier string.
    """
    unique_id = uuid.uuid4()
    if prefix:
        return f"{prefix}_{unique_id}"
    return str(unique_id)


def deep_merge_dicts(dict1: dict, dict2: dict) -> dict:
    """
    Recursively merges dict2 into dict1.

    It creates a new dictionary, leaving the original dictionaries unmodified.
    If keys conflict and both values are dictionaries, it merges them recursively.
    Otherwise, the value from dict2 overwrites the value from dict1.

    Args:
        dict1: The base dictionary.
        dict2: The dictionary to merge into the base dictionary.

    Returns:
        A new dictionary containing the merged key-value pairs.
    """
    merged = copy.deepcopy(dict1)
    for key, value in dict2.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = deep_merge_dicts(merged[key], value)
        else:
            merged[key] = value
    return merged


def parse_datetime_string(
    dt_string: str, formats: list[str] | None = None
) -> datetime.datetime | None:
    """
    Attempts to parse a datetime string into a datetime object.

    It tries a list of common ISO 8601 formats by default, but a custom
    list of format codes can be provided.

    Args:
        dt_string: The string representation of the datetime.
        formats: An optional list of format strings to try for parsing.

    Returns:
        A datetime object if parsing is successful, otherwise None.
        The returned datetime object will be timezone-aware if the input string
        contained timezone information.
    """
    if formats is None:
        # Default formats to try, from most to least specific
        formats = [
            "%Y-%m-%dT%H:%M:%S.%f%z",  # with microseconds and timezone
            "%Y-%m-%dT%H:%M:%S%z",     # without microseconds, with timezone
            "%Y-%m-%dT%H:%M:%S.%f",    # with microseconds, naive
            "%Y-%m-%dT%H:%M:%S",       # without microseconds, naive
            "%Y-%m-%d %H:%M:%S",       # space separated
        ]

    for fmt in formats:
        try:
            # Handle 'Z' for UTC
            if dt_string.endswith("Z"):
                dt_string = dt_string[:-1] + "+0000"
            return datetime.datetime.strptime(dt_string, fmt)
        except (ValueError, TypeError):
            continue

    return None