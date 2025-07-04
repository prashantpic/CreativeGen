from uuid import UUID
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from .. import schemas
from ....domain.services.credit_service import CreditService, InsufficientCreditsError
from ....dependencies import get_credit_service

router = APIRouter(prefix="/users/{user_id}/credits")

@router.get(
    "/balance",
    response_model=schemas.CreditBalanceResponseSchema,
    summary="Get User Credit Balance",
    description="Retrieves the current credit balance for a specific user."
)
async def get_credit_balance_for_user(
    user_id: UUID,
    credit_service: CreditService = Depends(get_credit_service)
):
    try:
        balance_domain = await credit_service.get_user_credit_balance(user_id)
        return schemas.CreditBalanceResponseSchema(
            user_id=balance_domain.user_id,
            balance=balance_domain.balance
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post(
    "/deduct",
    response_model=schemas.CreditDeductResponseSchema,
    summary="Deduct Credits for an Action",
    description="Deducts credits from a user's balance for performing a specific action. Fails if the user has insufficient credits."
)
async def deduct_credits_for_action(
    user_id: UUID,
    request: schemas.CreditDeductRequestSchema,
    credit_service: CreditService = Depends(get_credit_service)
):
    try:
        success = await credit_service.deduct_credits_for_action(
            user_id=user_id,
            action_type=request.action_type,
            reference_id=request.reference_id,
            advanced_params={"amount_override": request.amount_override} if request.amount_override else None
        )
        new_balance = await credit_service.get_user_credit_balance(user_id)
        return schemas.CreditDeductResponseSchema(
            success=success,
            new_balance=new_balance.balance,
            message="Credits deducted successfully." if success else "Failed to deduct credits."
        )
    except InsufficientCreditsError as e:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail={
                "message": str(e),
                "required_credits": str(e.required),
                "current_balance": str(e.balance)
            }
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get(
    "/cost",
    response_model=schemas.CreditCostResponseSchema,
    summary="Get Credit Cost for an Action",
    description="Retrieves the credit cost for a specific action, taking the user's current subscription plan into account (e.g., some actions may be free for Pro users)."
)
async def get_action_credit_cost(
    user_id: UUID,
    action_type: str = Query(..., description="The type of action, e.g., 'hd_export'."),
    credit_service: CreditService = Depends(get_credit_service)
):
    try:
        cost = await credit_service.get_credit_cost_for_action(user_id=user_id, action_type=action_type)
        return schemas.CreditCostResponseSchema(action_type=action_type, cost=cost)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))