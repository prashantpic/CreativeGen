"""
Contains common utility functions for working with Python collections.
"""
import collections.abc
from typing import Any, Dict, Generator, List, TypeVar

T_co = TypeVar("T_co", covariant=True)


def chunk_list(data: List[T_co], size: int) -> Generator[List[T_co], None, None]:
    """
    Yield successive n-sized chunks from a list.

    Args:
        data: The list to be chunked.
        size: The size of each chunk.

    Yields:
        A list representing the next chunk of the original list.

    Raises:
        ValueError: If the chunk size is not a positive integer.
    """
    if size <= 0:
        raise ValueError("Chunk size must be a positive integer.")
    for i in range(0, len(data), size):
        yield data[i : i + size]


def deep_merge_dicts(dict1: Dict[Any, Any], dict2: Dict[Any, Any]) -> Dict[Any, Any]:
    """
    Recursively merges dict2 into dict1 and returns a new dictionary.

    - If keys conflict and both values are dictionaries, they are merged.
    - Otherwise, the value from dict2 overwrites the value from dict1.
    - The original dictionaries are not modified.

    Args:
        dict1: The base dictionary.
        dict2: The dictionary to merge into the base.

    Returns:
        A new dictionary containing the merged key-value pairs.
    """
    merged = dict1.copy()
    for key, value in dict2.items():
        if key in merged and isinstance(
            merged[key], dict
        ) and isinstance(value, collections.abc.Mapping):
            merged[key] = deep_merge_dicts(merged[key], value)
        else:
            merged[key] = value
    return merged