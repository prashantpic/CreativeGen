```python
import uuid
from typing import Any, Dict, Optional

from .base_client import BaseClient


class AIGenerationClient(BaseClient):
    """
    HTTP client for interacting with the AI Generation Orchestration Service.
    """

    async def initiate_generation(
        self, payload: Dict[str, Any], headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Calls the endpoint to start a new generation task."""
        response = await self._request(
            method="POST", endpoint="/generations", json=payload, headers=headers
        )
        return response.json()

    async def get_generation_status(
        self, generation_id: uuid.UUID, headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Calls the endpoint to get the status of a generation task."""
        response = await self._request(
            method="GET",
            endpoint=f"/generations/{generation_id}",
            headers=headers,
        )
        return response.json()

# --- Singleton Management ---
ai_generation_client: AIGenerationClient

def init_client(base_url: str):
    """Initializes the singleton client instance."""
    global ai_generation_client
    ai_generation_client = AIGenerationClient(base_url=str(base_url))

async def close_client():
    """Closes the singleton client instance."""
    if 'ai_generation_client' in globals():
        await ai_generation_client.close()
```