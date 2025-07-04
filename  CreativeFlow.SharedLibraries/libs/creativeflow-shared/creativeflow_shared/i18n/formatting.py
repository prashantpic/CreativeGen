"""
Contains utilities for locale-aware formatting of dates, times, numbers, and currencies.
Ensures consistent presentation of data according to a user's locale.

Requirement Mapping: UI-006 (Multilingual Support - Backend Aspects)
"""

import datetime
import decimal

from babel import dates, numbers


def format_datetime_localized(
    dt: datetime.datetime, locale: str, format_name: str = "medium"
) -> str:
    """
    Formats a datetime object in a locale-aware manner.

    Args:
        dt: The datetime object to format.
        locale: The locale string (e.g., 'en_US', 'de_DE').
        format_name: The format name ('short', 'medium', 'long', 'full').

    Returns:
        The formatted datetime string.
    """
    return dates.format_datetime(dt, format=format_name, locale=locale)


def format_number_localized(
    number: int | float | decimal.Decimal, locale: str, pattern: str | None = None
) -> str:
    """
    Formats a number in a locale-aware manner.

    Args:
        number: The number to format.
        locale: The locale string (e.g., 'en_US', 'de_DE').
        pattern: An optional custom format pattern.

    Returns:
        The formatted number string.
    """
    return numbers.format_decimal(number, format=pattern, locale=locale)


def format_currency_localized(
    amount: decimal.Decimal, currency_code: str, locale: str
) -> str:
    """
    Formats a decimal amount as currency in a locale-aware manner.

    Args:
        amount: The decimal amount.
        currency_code: The 3-letter ISO currency code (e.g., 'USD', 'EUR').
        locale: The locale string (e.g., 'en_US', 'de_DE').

    Returns:
        The formatted currency string.
    """
    return numbers.format_currency(amount, currency_code, locale=locale)