"""
Initializer for the API routers package.

This module aggregates all version 1 API routers into a single `api_v1_router`
instance. This simplifies including all v1 routes in the main application file.
"""
from fastapi import APIRouter

from .consent_router import router as consent_api_router
from .data_privacy_router import router as data_privacy_api_router
from .user_profiles_router import router as user_profiles_api_router

api_v1_router = APIRouter()

api_v1_router.include_router(
    user_profiles_api_router, prefix="/profiles", tags=["User Profiles"]
)
api_v1_router.include_router(
    data_privacy_api_router, prefix="/privacy-requests", tags=["Data Privacy Requests"]
)
api_v1_router.include_router(
    consent_api_router, prefix="/consents", tags=["User Consents"]
)


__all__ = ["api_v1_router"]