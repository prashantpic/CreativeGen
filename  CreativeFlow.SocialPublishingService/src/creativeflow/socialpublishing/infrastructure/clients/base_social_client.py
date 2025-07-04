"""
Abstract base class for social media API clients.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

import httpx

from ...api.v1.schemas.publishing_schemas import GeneratedAsset
from ...application.exceptions import PlatformApiError
from ...config import Settings
from ._client_utils import map_platform_error


class BaseSocialClient(ABC):
    """
    Defines a common interface and shared utilities for social media platform
    API clients.
    """

    def __init__(
        self, http_client: httpx.AsyncClient, config: Settings, platform_name: str
    ):
        self.http_client = http_client
        self.config = config
        self.platform_name = platform_name

    async def _handle_api_error(self, response: httpx.Response):
        """
        Examines an error response and raises a standardized PlatformApiError.
        """
        try:
            response_json = response.json()
        except Exception:
            response_json = {"raw_response": response.text}
        
        raise map_platform_error(
            platform_name=self.platform_name,
            status_code=response.status_code,
            response_json=response_json,
        )

    @abstractmethod
    async def get_oauth_url(self, state: str, redirect_uri: str) -> str:
        """Get the platform's OAuth 2.0 authorization URL."""
        raise NotImplementedError

    @abstractmethod
    async def exchange_code_for_token(
        self, code: str, redirect_uri: str
    ) -> Dict[str, Any]:
        """
        Exchange an authorization code for an access token.
        Should return a dict with 'access_token', 'refresh_token', 'expires_in', 'scope'.
        """
        raise NotImplementedError

    @abstractmethod
    async def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refresh an expired access token using a refresh token.
        Should return a dict with 'access_token', 'expires_in', etc.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_user_profile(self, access_token: str) -> Dict[str, Any]:
        """
        Get the user's profile information from the platform.
        Should return a dict with 'id' and 'display_name'.
        """
        raise NotImplementedError
    
    @abstractmethod
    async def revoke_token(self, access_token: str) -> bool:
        """
        Revoke an access token, logging the user out.
        Returns True on success.
        """
        raise NotImplementedError

    @abstractmethod
    async def publish_content(
        self,
        access_token: str,
        text: Optional[str],
        assets: List[GeneratedAsset],
        options: Optional[Dict[str, Any]],
    ) -> str:
        """
        Publish content to the platform.
        Returns the URL or ID of the created post.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_trending_hashtags(
        self,
        access_token: Optional[str],
        keywords: List[str],
        industry: Optional[str],
        limit: int,
    ) -> List[Dict[str, Any]]:
        """
        Get trending hashtag suggestions.
        Returns a list of dicts, e.g., [{'tag': '#xyz', 'score': 0.9}].
        """
        raise NotImplementedError

    @abstractmethod
    async def get_best_post_times(self, access_token: str) -> List[Dict[str, Any]]:
        """
        Get best times to post based on user's account data.
        Returns a list of dicts, e.g., [{'day_of_week': 0, 'hour_of_day': 15, 'score': 0.8}].
        """
        raise NotImplementedError