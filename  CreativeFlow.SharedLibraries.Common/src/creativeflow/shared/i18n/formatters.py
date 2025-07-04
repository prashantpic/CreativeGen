"""
Provides locale-aware formatting functions for dates, times, numbers, and currencies.
"""
from datetime import date, datetime, time
from decimal import Decimal
from typing import Optional, Union

import babel.dates
import babel.numbers
import pytz


def _make_aware_if_needed(
    dt_obj: Union[datetime, time], timezone_str: Optional[str]
) -> Union[datetime, time]:
    """Helper to ensure a datetime object is timezone-aware."""
    if timezone_str:
        tz = pytz.timezone(timezone_str)
        if isinstance(dt_obj, datetime):
            if dt_obj.tzinfo is None:
                # Localize naive datetime
                return tz.localize(dt_obj)
            # Convert aware datetime to target timezone
            return dt_obj.astimezone(tz)
    return dt_obj


def format_datetime_localized(
    dt: datetime,
    locale_identifier: str,
    format_type: str = "medium",
    timezone: Optional[str] = None,
) -> str:
    """Formats a datetime object for a given locale and timezone."""
    aware_dt = _make_aware_if_needed(dt, timezone)
    tz_info_for_babel = pytz.timezone(timezone) if timezone else None
    return babel.dates.format_datetime(
        aware_dt, format=format_type, locale=locale_identifier, tzinfo=tz_info_for_babel
    )


def format_date_localized(
    d: date, locale_identifier: str, format_type: str = "medium"
) -> str:
    """Formats a date object for a given locale."""
    return babel.dates.format_date(d, format=format_type, locale=locale_identifier)


def format_time_localized(
    t: time,
    locale_identifier: str,
    format_type: str = "medium",
    timezone: Optional[str] = None,
) -> str:
    """Formats a time object for a given locale and timezone."""
    tz_info_for_babel = pytz.timezone(timezone) if timezone else None
    return babel.dates.format_time(
        t, format=format_type, locale=locale_identifier, tzinfo=tz_info_for_babel
    )


def format_number_localized(
    number: Union[int, float, Decimal], locale_identifier: str
) -> str:
    """Formats a number for a given locale."""
    if not isinstance(number, Decimal):
        number = Decimal(str(number))
    return babel.numbers.format_decimal(number, locale=locale_identifier)


def format_currency_localized(
    amount: Union[int, float, Decimal], currency_code: str, locale_identifier: str
) -> str:
    """Formats a currency value for a given locale."""
    if not isinstance(amount, Decimal):
        amount = Decimal(str(amount))
    return babel.numbers.format_currency(
        amount, currency_code, locale=locale_identifier
    )