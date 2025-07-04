```python
from typing import Any, Dict

from core.exceptions import ExternalServiceError
from domain.models.api_key import APIKey
from infrastructure.external_clients.user_team_client import UserTeamClient


class UserTeamProxyService:
    """
    Service to proxy requests to the internal User/Team Management Service.
    """

    def __init__(self, user_team_client: UserTeamClient):
        self.user_team_client = user_team_client

    async def proxy_get_user_details(self, api_client: APIKey) -> Dict[str, Any]:
        """
        Forwards the request to get the user's own details from the User/Team service.
        """
        try:
            # The user_id from the api_client is used to fetch the correct user.
            response_data = await self.user_team_client.get_user_details(
                user_id=api_client.user_id
            )
            return response_data
        except ExternalServiceError as e:
            raise e
```