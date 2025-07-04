import uuid
from typing import Any, Dict

from ....developer_platform.api.schemas import (
    asset_schemas,
    generation_schemas,
    user_team_schemas,
)
from ....developer_platform.core import exceptions
from ....developer_platform.domain.models.api_key import APIKey
from ....developer_platform.infrastructure.external_clients.ai_generation_client import (
    AIGenerationClient,
)
from ....developer_platform.infrastructure.external_clients.asset_management_client import (
    AssetManagementClient,
)
from ....developer_platform.infrastructure.external_clients.user_team_client import (
    UserTeamClient,
)


class GenerationProxyService:
    """
    Application service for proxying requests from API clients to internal
    generation, asset, and user/team services.
    """

    def __init__(
        self,
        ai_gen_client: AIGenerationClient,
        asset_mgmt_client: AssetManagementClient,
        user_team_client: UserTeamClient,
    ):
        """
        Initializes the GenerationProxyService.

        Args:
            ai_gen_client: Client for the AI Generation Orchestration Service.
            asset_mgmt_client: Client for the Asset Management Service.
            user_team_client: Client for the User/Team Management Service.
        """
        self.ai_gen_client = ai_gen_client
        self.asset_mgmt_client = asset_mgmt_client
        self.user_team_client = user_team_client

    async def proxy_initiate_generation(
        self, api_client: APIKey, payload: generation_schemas.GenerationCreateRequestSchema
    ) -> Dict[str, Any]:
        """
        Proxies a request to initiate a creative generation.

        Args:
            api_client: The authenticated API client making the request.
            payload: The request payload for the generation.

        Returns:
            The response from the AI Generation Orchestration Service.

        Raises:
            APIKeyPermissionDeniedError: If the API key lacks generation permissions.
        """
        if not api_client.permissions.can_generate_creative:
            raise exceptions.APIKeyPermissionDeniedError(
                detail="This API key cannot initiate generations."
            )
        
        # Here you might generate an internal, short-lived service-to-service
        # JWT token based on the api_client's identity (user_id) to pass to
        # downstream services for authenticated, authorized actions.
        # For now, we'll pass a placeholder.
        internal_auth_token = f"internal-token-for-user-{api_client.user_id}"

        return await self.ai_gen_client.initiate_generation(
            payload.model_dump(), internal_auth_token
        )

    async def proxy_get_generation_status(
        self, api_client: APIKey, generation_id: uuid.UUID
    ) -> Dict[str, Any]:
        """
        Proxies a request to get the status of a generation.

        Args:
            api_client: The authenticated API client making the request.
            generation_id: The ID of the generation to query.

        Returns:
            The response from the AI Generation Orchestration Service.
        """
        internal_auth_token = f"internal-token-for-user-{api_client.user_id}"
        return await self.ai_gen_client.get_generation_status(
            generation_id, internal_auth_token
        )
    
    async def proxy_retrieve_asset_details(
        self, api_client: APIKey, asset_id: uuid.UUID
    ) -> Dict[str, Any]:
        """
        Proxies a request to retrieve details for a specific asset.
        
        Args:
            api_client: The authenticated API client making the request.
            asset_id: The ID of the asset to retrieve.

        Returns:
            The response from the Asset Management Service.
            
        Raises:
            APIKeyPermissionDeniedError: If the API key lacks asset read permissions.
        """
        if not api_client.permissions.can_read_assets:
            raise exceptions.APIKeyPermissionDeniedError(
                detail="This API key cannot read asset details."
            )

        internal_auth_token = f"internal-token-for-user-{api_client.user_id}"
        return await self.asset_mgmt_client.get_asset_details(
            asset_id, internal_auth_token
        )

    async def proxy_get_user_details(
        self, api_client: APIKey, user_id_to_query: uuid.UUID
    ) -> Dict[str, Any]:
        """
        Proxies a request to retrieve user details.
        
        Args:
            api_client: The authenticated API client making the request.
            user_id_to_query: The ID of the user to retrieve details for.
            
        Returns:
            The response from the User/Team Management Service.
        
        Raises:
            APIKeyPermissionDeniedError: If the key lacks permission.
        """
        if not api_client.permissions.can_read_user_info:
            raise exceptions.APIKeyPermissionDeniedError(
                detail="This API key cannot read user information."
            )

        internal_auth_token = f"internal-token-for-user-{api_client.user_id}"
        return await self.user_team_client.get_user_details(
            user_id_to_query, internal_auth_token
        )