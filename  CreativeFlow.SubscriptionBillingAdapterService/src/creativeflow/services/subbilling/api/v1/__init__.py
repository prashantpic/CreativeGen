from fastapi import APIRouter
from .endpoints import subscriptions, credits, payments

# This main router for v1 aggregates all the endpoint-specific routers.
# It applies a common prefix to all routes defined within it.
api_v1_router = APIRouter(prefix="/api/v1")

# Include the subscriptions router
api_v1_router.include_router(
    subscriptions.router,
    tags=["Subscriptions"],
    # dependencies=[Depends(verify_internal_api_key)] # Optionally enforce security for the whole group
)

# Include the credits router
api_v1_router.include_router(
    credits.router,
    tags=["Credits"]
)

# Include the payments and billing utilities router
api_v1_router.include_router(
    payments.router,
    tags=["Payments"]
)