"""
Provides utilities for message localization using Python's standard `gettext` library.

This module allows loading translation files and retrieving translated strings
based on a key and locale.

Requirement Mapping: UI-006 (Multilingual Support - Backend Aspects)
"""
import gettext
import logging
import os
from typing import Callable

# Caches for loaded translation objects and the locale directory
_translations: dict[str, gettext.GNUTranslations] = {}
_locale_dir: str | None = None
_default_locale: str = "en_US"

logger = logging.getLogger(__name__)


def init_translations(locale_dir: str, domain: str = "messages") -> None:
    """
    Initializes the translation system by loading all available .mo files.

    This function should be called once at application startup. It scans the
    specified locale directory for language subdirectories and loads the
    compiled message files.

    Assumes a standard gettext directory structure:
    `locale_dir/<lang_code>/LC_MESSAGES/<domain>.mo`

    Args:
        locale_dir: The absolute path to the 'locales' directory.
        domain: The domain of the translation files (usually 'messages').
    """
    global _locale_dir, _translations
    _locale_dir = locale_dir
    _translations = {}

    if not os.path.isdir(_locale_dir):
        logger.warning(f"i18n locale directory not found: {_locale_dir}")
        return

    for lang_code in os.listdir(_locale_dir):
        if os.path.isdir(os.path.join(_locale_dir, lang_code)):
            try:
                translation = gettext.translation(
                    domain, localedir=_locale_dir, languages=[lang_code]
                )
                _translations[lang_code] = translation
                logger.info(f"Loaded translations for locale: {lang_code}")
            except FileNotFoundError:
                logger.warning(
                    f"No .mo file found for locale '{lang_code}' in domain '{domain}'."
                )


def get_translator(locale: str) -> Callable[[str], str]:
    """
    Retrieves a translation function for a given locale.

    The returned function takes a message key (the original string) and
    returns the translated string. It falls back to the default locale
    ('en_US') if the requested locale is not available, and ultimately
    returns the message key itself if no translations are found.

    Args:
        locale: The locale string (e.g., 'es_ES', 'fr_FR').

    Returns:
        A translator function (gettext).
    """
    translation = _translations.get(locale)
    if not translation:
        translation = _translations.get(_default_locale)

    if translation:
        return translation.gettext
    else:
        # Return a null translator that just returns the key
        return lambda msg: msg


def translate_message(message_key: str, locale: str, **kwargs) -> str:
    """
    Translates a message key for a specific locale and formats it with placeholders.

    Args:
        message_key: The message identifier (the original English string).
        locale: The target locale for translation.
        **kwargs: Placeholder values to format into the translated string.

    Returns:
        The translated and formatted message.
    """
    translator = get_translator(locale)
    translated_string = translator(message_key)

    if kwargs:
        try:
            return translated_string.format(**kwargs)
        except (KeyError, IndexError) as e:
            logger.error(
                f"Failed to format translated string for key '{message_key}' "
                f"in locale '{locale}'. Error: {e}"
            )
            # Return the unformatted string as a fallback
            return translated_string

    return translated_string