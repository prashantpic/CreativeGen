"""
Initializes the general utilities sub-package and exports its functions.
"""
from .collections import chunk_list, deep_merge_dicts
from .decorators import memoize, timed

__all__ = [
    # from .collections
    "chunk_list",
    "deep_merge_dicts",
    # from .decorators
    "timed",
    "memoize",
]