"""
Client for interacting with the Facebook Graph API.
"""
import logging
from typing import Any, Dict, List, Optional

from .base_social_client import BaseSocialClient

logger = logging.getLogger(__name__)


class FacebookClient(BaseSocialClient):
    """
    Implements methods to interact with Facebook Graph API for page management
    and content publishing.
    """

    def __init__(self, http_client, config):
        super().__init__(http_client, config, "facebook")

    async def get_oauth_url(self, state: str, redirect_uri: str) -> str:
        logger.warning("Method 'get_oauth_url' not implemented for FacebookClient.")
        raise NotImplementedError

    async def exchange_code_for_token(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        logger.warning("Method 'exchange_code_for_token' not implemented for FacebookClient.")
        raise NotImplementedError

    async def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        logger.warning("Method 'refresh_access_token' not implemented for FacebookClient.")
        raise NotImplementedError

    async def get_user_profile(self, access_token: str) -> Dict[str, Any]:
        logger.warning("Method 'get_user_profile' not implemented for FacebookClient.")
        raise NotImplementedError

    async def revoke_token(self, access_token: str) -> bool:
        logger.warning("Method 'revoke_token' not implemented for FacebookClient.")
        raise NotImplementedError

    async def publish_content(
        self,
        access_token: str,
        text: Optional[str],
        assets: List[Dict[str, Any]],
        options: Optional[Dict[str, Any]],
    ) -> str:
        logger.warning("Method 'publish_content' not implemented for FacebookClient.")
        raise NotImplementedError

    async def get_trending_hashtags(
        self, access_token: Optional[str], keywords: List[str], industry: Optional[str], limit: int
    ) -> List[Dict[str, Any]]:
        logger.warning("Method 'get_trending_hashtags' not supported by Facebook API.")
        raise NotImplementedError

    async def get_best_post_times(self, access_token: str) -> List[Dict[str, Any]]:
        logger.warning("Method 'get_best_post_times' not implemented for FacebookClient.")
        raise NotImplementedError