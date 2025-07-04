```python
import uuid
from typing import Any, Dict

from api.schemas.generation_schemas import GenerationCreateRequestSchema
from core.exceptions import ExternalServiceError
from domain.models.api_key import APIKey
from infrastructure.external_clients.ai_generation_client import AIGenerationClient


class GenerationProxyService:
    """
    Service to proxy requests to the internal AI Generation Orchestration Service.
    """

    def __init__(self, ai_gen_client: AIGenerationClient):
        self.ai_gen_client = ai_gen_client

    async def proxy_initiate_generation(
        self, api_client: APIKey, payload: GenerationCreateRequestSchema
    ) -> Dict[str, Any]:
        """
        Forwards the generation initiation request to the AI Generation service.
        """
        try:
            # Here we might inject an internal service-to-service auth token
            # representing the user associated with the api_client.
            # For now, we'll pass the request through without it.
            response_data = await self.ai_gen_client.initiate_generation(
                payload=payload.model_dump()
            )
            return response_data
        except ExternalServiceError as e:
            # Re-raise or handle specific errors from the downstream service
            raise e

    async def proxy_get_generation_status(
        self, api_client: APIKey, generation_id: uuid.UUID
    ) -> Dict[str, Any]:
        """
        Forwards the request to get generation status to the AI Generation service.
        """
        try:
            # The client needs to ensure that the user associated with api_client
            # has permission to view this generation_id. This logic resides
            # in the downstream service.
            response_data = await self.ai_gen_client.get_generation_status(
                generation_id=generation_id
            )
            return response_data
        except ExternalServiceError as e:
            raise e
```