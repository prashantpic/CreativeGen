"""
Initializes the 'i18n' (internationalization) submodule.
Exports utilities for formatting and localization.

Requirement Mapping: UI-006 (Multilingual Support - Backend Aspects)
"""
from .formatting import (
    format_currency_localized,
    format_datetime_localized,
    format_number_localized,
)
from .translation import get_translator, init_translations, translate_message

__all__ = [
    "format_datetime_localized",
    "format_number_localized",
    "format_currency_localized",
    "get_translator",
    "translate_message",
    "init_translations",
]