"""
Contains utilities for sanitizing user inputs and encoding outputs
to prevent common vulnerabilities like Cross-Site Scripting (XSS).
"""
import html
import re

import bleach

# A restrictive set of tags for general user input, allowing basic formatting.
DEFAULT_ALLOWED_TAGS = {"p", "b", "strong", "i", "em", "u", "ol", "ul", "li", "br"}


def sanitize_html_input(
    html_string: str,
    allowed_tags: list | None = None,
    allowed_attributes: dict | None = None,
    strip_comments: bool = True,
) -> str:
    """
    Strips potentially dangerous HTML from a string using bleach.

    Args:
        html_string: The input string containing HTML.
        allowed_tags: A list of allowed HTML tags. Defaults to a safe subset.
        allowed_attributes: A dictionary of allowed attributes per tag. Defaults to none.
        strip_comments: Whether to remove HTML comments.

    Returns:
        The sanitized HTML string.
    """
    if allowed_tags is None:
        allowed_tags = list(DEFAULT_ALLOWED_TAGS)
    if allowed_attributes is None:
        allowed_attributes = {}

    return bleach.clean(
        html_string,
        tags=allowed_tags,
        attributes=allowed_attributes,
        strip=True,  # Strip disallowed tags instead of escaping them
        strip_comments=strip_comments,
    )


def encode_for_html_attribute(text: str) -> str:
    """
    Encodes a string for safe inclusion in an HTML attribute value.

    This is important for preventing XSS when user-controlled data is placed
    inside attributes like `value`, `title`, or `alt`.

    Args:
        text: The text to encode.

    Returns:
        The HTML-escaped string.
    """
    return html.escape(text, quote=True)


def clean_filename(filename: str) -> str:
    """
    Sanitizes a filename to remove or replace potentially unsafe characters.

    This helps prevent path traversal attacks and issues with file systems.
    It removes characters like slashes and colons, and collapses multiple
    dots or spaces.

    Args:
        filename: The original filename.

    Returns:
        A sanitized version of the filename.
    """
    # Remove path traversal sequences
    sanitized = filename.replace("..", "")

    # Remove or replace invalid characters for most file systems
    # (keeps letters, numbers, hyphens, underscores, dots)
    sanitized = re.sub(r'[\\/*?:"<>|]', "", sanitized)

    # Replace multiple spaces with a single underscore
    sanitized = re.sub(r"\s+", "_", sanitized)

    # Limit length to prevent issues with file systems
    max_length = 200
    if len(sanitized) > max_length:
        name, ext = os.path.splitext(sanitized)
        sanitized = name[: max_length - len(ext)] + ext

    # Ensure it's not empty
    if not sanitized:
        return "unnamed_file"

    return sanitized