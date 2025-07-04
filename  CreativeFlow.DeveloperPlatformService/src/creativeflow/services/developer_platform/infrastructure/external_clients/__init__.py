"""
Infrastructure Layer: External Clients Package

This package contains HTTP clients for interacting with other microservices
or external APIs. Each client encapsulates the logic for communicating with a
specific service, including handling authentication, retries, and error mapping.
"""

from .ai_generation_client import AIGenerationClient
from .asset_management_client import AssetManagementClient
from .base_client import BaseClient
from .user_team_client import UserTeamClient

__all__ = [
    "BaseClient",
    "AIGenerationClient",
    "AssetManagementClient",
    "UserTeamClient"
]