"""
Defines the FastAPI router for handling AI generation requests. Includes the
endpoint for initiating a new creative generation workflow.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from ....service.aigeneration_orchestrator.app.dtos import (
    GenerationInitiatedResponseDTO, GenerationRequestCreateDTO)
from ....service.aigeneration_orchestrator.app.use_cases.initiate_generation import (
    InitiateGenerationUseCase, InsufficientCreditsError)
from ..dependencies import get_initiate_generation_use_case, get_user_id_from_token

router = APIRouter()


@router.post(
    "/",
    response_model=GenerationInitiatedResponseDTO,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Initiate Creative Generation",
    description="Starts a new AI creative generation workflow after validating user credits.",
    responses={
        400: {"description": "Invalid request body"},
        401: {"description": "Invalid or missing JWT"},
        402: {"description": "Insufficient credits for the operation"},
        500: {"description": "Unexpected service error"},
    },
)
async def initiate_creative_generation(
    request: GenerationRequestCreateDTO,
    user_id: UUID = Depends(get_user_id_from_token),
    use_case: InitiateGenerationUseCase = Depends(get_initiate_generation_use_case),
):
    """
    Handles the API request to start a new generation.

    It depends on the `InitiateGenerationUseCase` to perform the business logic.
    It catches specific business exceptions and maps them to appropriate HTTP
    status codes.
    """
    try:
        generation_request = await use_case.execute(user_id, request)
        return GenerationInitiatedResponseDTO(generationId=generation_request.id)
    except InsufficientCreditsError as e:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=str(e),
        )
    except Exception as e:
        # Catch-all for other unexpected errors during use case execution
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while initiating the generation.",
        ) from e