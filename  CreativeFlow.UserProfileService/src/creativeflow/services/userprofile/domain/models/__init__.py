"""
Initializer for domain model entities and value objects.

This file marks the 'models' directory as a Python package and exports
the key domain models for convenient access from other modules.
"""
from .consent import Consent, ConsentType
from .data_privacy import DataPrivacyRequest, RetentionRule, DataPrivacyRequestType, DataPrivacyRequestStatus, RetentionRuleAction
from .user_profile import Preferences, UserProfile

__all__ = [
    "UserProfile",
    "Preferences",
    "Consent",
    "ConsentType",
    "DataPrivacyRequest",
    "DataPrivacyRequestType",
    "DataPrivacyRequestStatus",
    "RetentionRule",
    "RetentionRuleAction",
]