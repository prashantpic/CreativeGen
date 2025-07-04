from enum import Enum
from typing import Optional
from uuid import UUID
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field

class SubscriptionTier(str, Enum):
    """Enumeration for subscription plan tiers."""
    FREE = "Free"
    PRO = "Pro"
    TEAM = "Team"
    ENTERPRISE = "Enterprise"

class SubscriptionStatus(str, Enum):
    """Enumeration for the status of a user's subscription."""
    ACTIVE = "Active"
    TRIAL = "Trial"
    SUSPENDED = "Suspended"  # e.g., due to failed payment
    CANCELLED = "Cancelled"  # Will expire at period end
    EXPIRED = "Expired"      # Past period end and inactive

class FreemiumLimits(BaseModel):
    """Defines the usage limits for a user on the Free tier."""
    monthly_generations_limit: int = Field(100, description="Max generations per month for free users.")
    generations_used_this_month: int = Field(..., description="Generations consumed in the current billing cycle.")
    watermarked_exports: bool = Field(True, description="Whether exports have a watermark.")
    basic_templates_only: bool = Field(True, description="Whether user is restricted to basic templates.")

class PlanFeatures(BaseModel):
    """Defines the features available in a given subscription plan."""
    name: str = Field(..., description="The public name of the plan.")
    price_monthly: Optional[Decimal] = Field(None, description="Monthly price of the plan.")
    unlimited_standard_generations: bool = Field(False, description="Whether standard generations are unlimited.")
    brand_kit_access: bool = Field(False, description="Access to Brand Kit features.")
    hd_exports: bool = Field(False, description="Ability to export in High Definition.")
    priority_support: bool = Field(False, description="Access to priority customer support.")
    collaboration_tools: bool = Field(False, description="Access to real-time collaboration tools.")
    team_management: bool = Field(False, description="Ability to manage team members.")
    advanced_analytics: bool = Field(False, description="Access to advanced analytics dashboard.")
    sso_access: bool = Field(False, description="Availability of Single Sign-On (SSO).")
    custom_branding: bool = Field(False, description="Ability to use custom branding (white-label).")
    dedicated_account_manager: bool = Field(False, description="Assignment of a dedicated account manager.")

class UserSubscriptionDomain(BaseModel):
    """
    A comprehensive internal domain model representing a user's subscription state.
    This model is constructed by the service layer by combining data from Odoo and
    internal business logic.
    """
    user_id: UUID = Field(..., description="The user's platform ID.")
    odoo_subscription_id: Optional[str] = Field(None, description="The subscription ID from Odoo (e.g., 'SO123').")
    current_plan_id: str = Field(..., description="Internal identifier for the plan (e.g., 'pro_monthly').")
    current_plan_name: str = Field(..., description="Public display name of the plan.")
    status: SubscriptionStatus = Field(..., description="The current status of the subscription.")
    current_period_start: Optional[datetime] = Field(None, description="Start date of the current billing cycle.")
    current_period_end: Optional[datetime] = Field(None, description="End date of the current billing cycle (when the next charge is due or subscription expires).")
    features: PlanFeatures = Field(..., description="A detailed breakdown of features included in the current plan.")
    freemium_limits: Optional[FreemiumLimits] = Field(None, description="Usage limits, applicable only if the user is on the Free tier.")