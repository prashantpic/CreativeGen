```python
from fastapi import APIRouter

from .routers import (
    api_keys_router,
    webhooks_router,
    usage_router,
    generation_proxy_router,
    asset_proxy_router,
    user_team_proxy_router,
)

api_router = APIRouter()

# Include all the individual routers
api_router.include_router(api_keys_router.router)
api_router.include_router(webhooks_router.router)
api_router.include_router(usage_router.router)
api_router.include_router(generation_proxy_router.router)
api_router.include_router(asset_proxy_router.router)
api_router.include_router(user_team_proxy_router.router)
```