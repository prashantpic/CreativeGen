from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas
from ....domain.services.subscription_service import SubscriptionService
from ....dependencies import get_subscription_service
from ....domain.models.subscription_models import FreemiumLimits

router = APIRouter(prefix="/users/{user_id}/subscription")

@router.get(
    "/",
    response_model=schemas.UserSubscriptionResponseSchema,
    summary="Get User Subscription Status",
    description="Retrieves the detailed subscription status for a specific user, including their current plan, features, and billing cycle information."
)
async def get_subscription_status_for_user(
    user_id: UUID,
    sub_service: SubscriptionService = Depends(get_subscription_service)
):
    try:
        sub_domain = await sub_service.get_user_subscription_status(user_id)
        # Manually map domain model to response schema if they differ significantly
        # For simple cases, FastAPI can handle it with from_attributes = True
        remaining = None
        if sub_domain.freemium_limits:
            remaining = sub_domain.freemium_limits.monthly_generations_limit - sub_domain.freemium_limits.generations_used_this_month
        
        return schemas.UserSubscriptionResponseSchema(
            user_id=sub_domain.user_id,
            current_plan_id=sub_domain.current_plan_id,
            current_plan_name=sub_domain.current_plan_name,
            status=sub_domain.status.value,
            current_period_end=sub_domain.current_period_end,
            features=sub_domain.features,
            freemium_generations_remaining=remaining
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put(
    "/",
    response_model=schemas.UserSubscriptionResponseSchema,
    summary="Update User Subscription",
    description="Updates a user's subscription to a new plan. This handles both upgrades and downgrades."
)
async def update_user_subscription(
    user_id: UUID,
    request: schemas.SubscriptionUpdateRequestSchema,
    sub_service: SubscriptionService = Depends(get_subscription_service)
):
    try:
        # Business logic to determine 'action' (upgrade/downgrade) would go here
        # For simplicity, we pass a generic 'update' action and let Odoo decide.
        action = "update" 
        updated_sub = await sub_service.process_subscription_change(user_id, request.new_plan_id, action)
        return updated_sub
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete(
    "/",
    response_model=schemas.UserSubscriptionResponseSchema,
    summary="Cancel User Subscription",
    description="Cancels a user's active subscription. The subscription will remain active until the end of the current billing period."
)
async def cancel_user_subscription(
    user_id: UUID,
    sub_service: SubscriptionService = Depends(get_subscription_service)
):
    try:
        # When cancelling, the 'new_plan_id' is irrelevant, but the service method may need it.
        # We can pass a placeholder or refactor the service method.
        current_sub = await sub_service.get_user_subscription_status(user_id)
        cancelled_sub = await sub_service.process_subscription_change(user_id, current_sub.current_plan_id, "cancel")
        return cancelled_sub
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get(
    "/freemium-limits",
    response_model=FreemiumLimits,
    summary="Get User Freemium Limits",
    description="Retrieves the current usage and limits for a user on the freemium plan."
)
async def get_user_freemium_limits(
    user_id: UUID,
    sub_service: SubscriptionService = Depends(get_subscription_service)
):
    try:
        return await sub_service.get_freemium_usage(user_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))