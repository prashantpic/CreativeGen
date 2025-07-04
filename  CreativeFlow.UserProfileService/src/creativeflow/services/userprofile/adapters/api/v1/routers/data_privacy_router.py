"""
HTTP endpoints for managing GDPR/CCPA data privacy requests.
"""
from fastapi import APIRouter, Depends, Path, status
from uuid import UUID

from .....application.services.data_privacy_service import DataPrivacyService
from ..dependencies import get_data_privacy_service
from ..schemas import DataPrivacyRequestResponseSchema

router = APIRouter()


@router.post(
    "/{auth_user_id}/access-request",
    response_model=DataPrivacyRequestResponseSchema,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Submit Data Access Request",
    description="Submit a request for access to all personal data held about the user.",
)
async def submit_data_access_request_endpoint(
    auth_user_id: str = Path(..., description="Authenticated User ID"),
    service: DataPrivacyService = Depends(get_data_privacy_service),
) -> DataPrivacyRequestResponseSchema:
    """Endpoint to submit a data access request."""
    return await service.request_data_access(auth_user_id)


@router.post(
    "/{auth_user_id}/portability-request",
    response_model=DataPrivacyRequestResponseSchema,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Submit Data Portability Request",
    description="Submit a request for personal data in a machine-readable format.",
)
async def submit_data_portability_request_endpoint(
    auth_user_id: str = Path(..., description="Authenticated User ID"),
    service: DataPrivacyService = Depends(get_data_privacy_service),
) -> DataPrivacyRequestResponseSchema:
    """Endpoint to submit a data portability request."""
    return await service.request_data_portability(auth_user_id)


@router.post(
    "/{auth_user_id}/deletion-request",
    response_model=DataPrivacyRequestResponseSchema,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Submit Account Deletion Request",
    description="Submit a request to have all personal data deleted (Right to be Forgotten).",
)
async def submit_account_deletion_request_endpoint(
    auth_user_id: str = Path(..., description="Authenticated User ID"),
    service: DataPrivacyService = Depends(get_data_privacy_service),
) -> DataPrivacyRequestResponseSchema:
    """Endpoint to submit an account deletion request."""
    return await service.request_account_deletion(auth_user_id)

# The SDS mentions a GET endpoint for status, but the current service design
# does not include a `get_request_by_id` method. This could be added later.
# @router.get("/{auth_user_id}/requests/{request_id}") ...