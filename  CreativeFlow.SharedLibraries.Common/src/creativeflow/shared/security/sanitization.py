"""
Provides output sanitization utilities, especially for HTML content.
"""
from typing import Dict, List, Optional

import bleach

# A safe default set of allowed HTML tags for user-generated content.
DEFAULT_ALLOWED_TAGS: List[str] = [
    "p", "br", "b", "i", "u", "strong", "em", "a", "ul", "ol", "li",
    "blockquote", "code", "pre", "h1", "h2", "h3", "h4", "h5", "h6",
    "img", "span", "div",
]

# A safe default set of allowed attributes for the allowed tags.
# The wildcard '*' applies to all tags.
DEFAULT_ALLOWED_ATTRIBUTES: Dict[str, List[str]] = {
    "a": ["href", "title", "target"],
    "img": ["src", "alt", "title", "width", "height"],
    "*": ["class", "id"],  # Note: 'style' is excluded by default for security.
}


def sanitize_html_output(
    html_string: str,
    custom_allowed_tags: Optional[List[str]] = None,
    custom_allowed_attributes: Optional[Dict[str, List[str]]] = None,
    strip_comments: bool = True,
) -> str:
    """
    Sanitizes an HTML string to prevent XSS attacks.

    This function uses bleach to remove any HTML tags and attributes that are
    not explicitly allowed.

    Args:
        html_string: The HTML string to sanitize.
        custom_allowed_tags: An optional list of allowed HTML tags to override
                             the default safe set.
        custom_allowed_attributes: An optional dictionary of allowed attributes
                                   per tag to override the default.
        strip_comments: If True (default), HTML comments are removed.

    Returns:
        The sanitized HTML string. Returns an empty string if the input is
        invalid.
    """
    if not html_string or not isinstance(html_string, str):
        return ""

    tags_to_allow = (
        custom_allowed_tags
        if custom_allowed_tags is not None
        else DEFAULT_ALLOWED_TAGS
    )
    attrs_to_allow = (
        custom_allowed_attributes
        if custom_allowed_attributes is not None
        else DEFAULT_ALLOWED_ATTRIBUTES
    )

    return bleach.clean(
        html_string,
        tags=tags_to_allow,
        attributes=attrs_to_allow,
        strip=True,  # Strips disallowed tags entirely instead of escaping them
        strip_comments=strip_comments,
    )