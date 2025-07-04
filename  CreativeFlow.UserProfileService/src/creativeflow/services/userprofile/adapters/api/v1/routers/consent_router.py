"""
HTTP endpoints for user consent management.
"""
from typing import List

from fastapi import APIRouter, Depends, Path

from .....application.services.consent_service import ConsentService
from ..dependencies import get_consent_service
from ..schemas import (ConsentResponseSchema, ConsentTypeEnum,
                       ConsentUpdateRequestSchema)

router = APIRouter()


@router.get(
    "/{auth_user_id}/consents",
    response_model=List[ConsentResponseSchema],
    summary="Get All User Consents",
    description="Retrieve a list of all consent statuses for a specific user.",
)
async def get_user_consents_endpoint(
    auth_user_id: str = Path(..., description="Authenticated User ID"),
    service: ConsentService = Depends(get_consent_service),
) -> List[ConsentResponseSchema]:
    """
    Endpoint to retrieve all consents for a user.
    """
    return await service.get_user_consents(auth_user_id=auth_user_id)


@router.put(
    "/{auth_user_id}/consents/{consent_type}",
    response_model=ConsentResponseSchema,
    summary="Update a User Consent",
    description="Grant or withdraw a specific type of consent for a user.",
)
async def update_user_consent_endpoint(
    consent_in: ConsentUpdateRequestSchema,
    auth_user_id: str = Path(..., description="Authenticated User ID"),
    consent_type: ConsentTypeEnum = Path(
        ..., description="The type of consent to update"
    ),
    service: ConsentService = Depends(get_consent_service),
) -> ConsentResponseSchema:
    """
    Endpoint to update (grant or withdraw) a specific consent.
    """
    return await service.update_user_consent(
        auth_user_id=auth_user_id, consent_type=consent_type, consent_update=consent_in
    )