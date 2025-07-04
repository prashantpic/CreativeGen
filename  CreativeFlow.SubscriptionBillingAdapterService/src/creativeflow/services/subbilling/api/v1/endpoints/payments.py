from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status

from .. import schemas
from ....domain.services.payment_orchestration_service import PaymentOrchestrationService
from ....dependencies import get_payment_orchestration_service

router = APIRouter(prefix="/users/{user_id}/payments")

@router.get(
    "/manage-methods-url",
    response_model=schemas.PaymentMethodUpdateLinkResponseSchema,
    summary="Get Payment Method Management URL",
    description="Provides a URL for the user to manage their payment methods (e.g., update credit card). This may link to Stripe, PayPal, or the Odoo customer portal."
)
async def get_payment_method_update_url(
    user_id: UUID,
    return_url: str = Query(..., description="The URL to return the user to after they are done."),
    provider: str = Query(default="stripe", enum=["stripe", "paypal"]),
    payment_service: PaymentOrchestrationService = Depends(get_payment_orchestration_service)
):
    url = await payment_service.get_payment_method_update_url(user_id, provider, return_url)
    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not generate a payment management URL for provider '{provider}'. Fallback to Odoo portal might be unavailable."
        )
    return schemas.PaymentMethodUpdateLinkResponseSchema(update_url=url)


@router.get(
    "/invoices",
    response_model=schemas.InvoiceListResponseSchema,
    summary="List User Invoices",
    description="Retrieves a list of the user's past invoices from Odoo."
)
async def list_user_invoices(
    user_id: UUID,
    limit: int = Query(10, ge=1, le=50, description="The maximum number of invoices to return."),
    payment_service: PaymentOrchestrationService = Depends(get_payment_orchestration_service)
):
    try:
        invoices = await payment_service.list_user_invoices(user_id, limit)
        return schemas.InvoiceListResponseSchema(invoices=invoices)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post(
    "/tax-preview",
    response_model=schemas.TaxCalculationResponseSchema,
    summary="Get Tax Information for Purchase Preview",
    description="Calculates and returns the estimated tax for a potential purchase based on the user's location and the items being purchased. All calculations are performed by Odoo."
)
async def get_tax_info_for_purchase_preview(
    user_id: UUID,
    request: schemas.TaxCalculationRequestSchema,
    payment_service: PaymentOrchestrationService = Depends(get_payment_orchestration_service)
):
    try:
        tax_info = await payment_service.get_tax_information_for_purchase(user_id, request.model_dump())
        return schemas.TaxCalculationResponseSchema(**tax_info)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))