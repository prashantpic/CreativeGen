"""
Contains utility functions for internationalization (i18n).
"""
from datetime import datetime
from typing import List, Optional

import pytz
from babel import Locale, negotiate_locale

DEFAULT_SUPPORTED_LOCALES: List[str] = [
    "en_US", "en_GB", "es_ES", "es_MX", "fr_FR", "de_DE"
]
DEFAULT_LOCALE: str = "en_US"


def get_user_locale(
    user_preference: Optional[str] = None,
    accept_language_header: Optional[str] = None,
    supported_locales: List[str] = None,
    default_locale: str = DEFAULT_LOCALE,
) -> str:
    """
    Determines the best locale based on user preference and request headers.

    The resolution order is:
    1. A valid `user_preference` if provided.
    2. The best match from the `accept_language_header` against supported locales.
    3. The `default_locale`.

    Args:
        user_preference: The user's explicitly saved locale preference.
        accept_language_header: The 'Accept-Language' HTTP header value.
        supported_locales: A list of supported locale strings.
        default_locale: The fallback locale if no match is found.

    Returns:
        The negotiated locale string.
    """
    locales_to_use = supported_locales if supported_locales else DEFAULT_SUPPORTED_LOCALES

    if user_preference and user_preference in locales_to_use:
        return user_preference

    if accept_language_header:
        # `negotiate_locale` finds the best match from the header.
        negotiated = negotiate_locale(
            [lang.split(';')[0].strip() for lang in accept_language_header.split(',')],
            locales_to_use
        )
        if negotiated:
            return negotiated

    return default_locale


def get_timezone_aware_datetime(
    dt_object: datetime,
    target_timezone_str: str,
    source_timezone_str: Optional[str] = None,
) -> datetime:
    """
    Converts a datetime object to a target timezone.

    - If `dt_object` is naive and `source_timezone_str` is provided, it's
      localized to the source timezone first.
    - If `dt_object` is naive and no `source_timezone_str` is given, it is
      assumed to be in UTC.
    - If `dt_object` is already timezone-aware, it's directly converted.

    Args:
        dt_object: The datetime object to convert.
        target_timezone_str: The IANA timezone string for the target timezone.
        source_timezone_str: The IANA timezone string for the source if naive.

    Returns:
        A new timezone-aware datetime object in the target timezone.
    """
    target_tz = pytz.timezone(target_timezone_str)

    if dt_object.tzinfo is None:  # Naive datetime object
        if source_timezone_str:
            source_tz = pytz.timezone(source_timezone_str)
            aware_dt = source_tz.localize(dt_object)
        else:  # Assume UTC if naive and no source timezone is specified
            aware_dt = pytz.utc.localize(dt_object)
    else:  # Already aware
        aware_dt = dt_object

    return aware_dt.astimezone(target_tz)