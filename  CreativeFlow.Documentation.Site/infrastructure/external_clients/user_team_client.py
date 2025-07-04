```python
import uuid
from typing import Any, Dict

from .base_client import BaseExternalClient


class UserTeamClient(BaseExternalClient):
    """
    HTTP client for interacting with the User/Team Management Service.
    """
    _service_name = "UserTeamService"

    async def get_user_details(self, user_id: uuid.UUID) -> Dict[str, Any]:
        """
        Calls the downstream service to retrieve details for a specific user.
        In a real scenario, this would likely require an internal service-to-service
        authentication token in the headers.
        """
        # The endpoint might be `/users/{user_id}` or similar
        return await self._request("GET", f"/users/{user_id}")

    # Add other methods like list_user_teams, get_team_details, etc. as needed.


# Singleton instance
user_team_client = UserTeamClient()
```