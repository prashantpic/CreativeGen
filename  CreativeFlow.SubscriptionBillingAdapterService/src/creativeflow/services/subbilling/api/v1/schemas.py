from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime, date
from decimal import Decimal
from typing import List, Optional, Dict, Any

# --- Subscription Schemas ---

class SubscriptionPlanInfoSchema(BaseModel):
    """Corresponds to the PlanFeatures domain model for API responses."""
    name: str
    price_monthly: Optional[Decimal] = None
    unlimited_standard_generations: bool
    brand_kit_access: bool
    hd_exports: bool
    priority_support: bool
    team_management: bool

    class Config:
        from_attributes = True

class UserSubscriptionResponseSchema(BaseModel):
    """Response schema for a user's subscription status."""
    user_id: UUID
    current_plan_id: str
    current_plan_name: str
    status: str
    current_period_end: Optional[datetime] = None
    features: SubscriptionPlanInfoSchema
    freemium_generations_remaining: Optional[int] = None

    class Config:
        from_attributes = True

class SubscriptionUpdateRequestSchema(BaseModel):
    """Request schema for updating a user's subscription plan."""
    new_plan_id: str = Field(..., description="The identifier of the new plan to switch to (e.g., 'pro_monthly' or Odoo product ID).")


# --- Credit Schemas ---

class CreditBalanceResponseSchema(BaseModel):
    """Response schema for a user's credit balance."""
    user_id: UUID
    balance: Decimal
    currency: str = "Credits"

class CreditDeductRequestSchema(BaseModel):
    """Request schema for deducting credits for a specific action."""
    action_type: str = Field(..., description="Identifier for the action, e.g., 'hd_export'.")
    reference_id: Optional[str] = Field(None, description="Optional ID of the related entity, e.g., a generation request UUID.")
    amount_override: Optional[Decimal] = Field(None, description="For variable cost actions, specify the exact amount to deduct.")

class CreditDeductResponseSchema(BaseModel):
    """Response schema after a credit deduction attempt."""
    success: bool
    new_balance: Decimal
    message: Optional[str] = None

class CreditCostResponseSchema(BaseModel):
    """Response schema for the cost of an action."""
    action_type: str
    cost: Decimal

class InsufficientCreditsResponseSchema(BaseModel):
    """Response schema when a user has insufficient credits."""
    message: str
    required_credits: Decimal
    current_balance: Decimal
    upgrade_options: List[Dict[str, Any]] = Field(default_factory=list, description="List of suggested plans to upgrade to.")


# --- Payment & Billing Schemas ---

class PaymentMethodUpdateLinkResponseSchema(BaseModel):
    """Response schema containing a URL to update payment methods."""
    update_url: str

class InvoiceSummarySchema(BaseModel):
    """A summary of a single invoice."""
    invoice_id: str
    date: Optional[date]
    total_amount: Decimal
    status: str
    pdf_url: Optional[str] = None

class InvoiceListResponseSchema(BaseModel):
    """Response schema for a list of invoices."""
    invoices: List[InvoiceSummarySchema]

class TaxCalculationRequestSchema(BaseModel):
    """Request schema for calculating tax on a potential purchase."""
    items: List[Dict[str, Any]] = Field(..., description="List of items, e.g., [{'product_id': 123, 'quantity': 1}]")
    customer_address: Optional[Dict[str, Any]] = Field(None, description="Customer address for tax calculation, e.g., {'country_id': 'US', 'zip': '90210'}")

class TaxCalculationResponseSchema(BaseModel):
    """Response schema with calculated tax information."""
    subtotal: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    tax_breakdown: List[Dict[str, Any]] = Field(default_factory=list)