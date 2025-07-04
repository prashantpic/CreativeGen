from datetime import datetime
from decimal import Decimal
from typing import Dict, Any, Optional, List
from uuid import UUID

from ..models.subscription_models import UserSubscriptionDomain, PlanFeatures, SubscriptionStatus, FreemiumLimits
from ..models.credit_models import CreditBalanceDomain

class OdooMappingService:
    """
    A service dedicated to mapping data structures between this adapter's
    internal domain/API models and the formats expected by/returned from Odoo.
    This acts as an anti-corruption layer.
    """

    def from_odoo_subscription_to_domain(self, user_id: UUID, odoo_data: Optional[Dict[str, Any]]) -> UserSubscriptionDomain:
        """Maps an Odoo subscription dictionary to our internal UserSubscriptionDomain model."""
        if not odoo_data:
            # Default to a Free plan if no subscription data is found in Odoo
            return self._get_default_free_plan(user_id)

        # Mapping Odoo's stage concept to our SubscriptionStatus enum
        stage_name = odoo_data.get('stage_id', [0, 'Cancelled'])[1] # stage_id is often a tuple (id, name)
        status = self._map_odoo_stage_to_status(stage_name)
        
        # Odoo dates can be False if not set
        start_date = odoo_data.get('date_start')
        end_date = odoo_data.get('recurring_next_date')

        plan_features = self.from_odoo_plan_product_to_features(odoo_data.get('template_id', {}))

        return UserSubscriptionDomain(
            user_id=user_id,
            odoo_subscription_id=odoo_data.get('code'),
            current_plan_id=str(odoo_data.get('template_id', [0])[0]), # Get the ID from the tuple
            current_plan_name=plan_features.name,
            status=status,
            current_period_start=datetime.fromisoformat(start_date) if start_date else None,
            current_period_end=datetime.fromisoformat(end_date) if end_date else None,
            features=plan_features,
            freemium_limits=FreemiumLimits(generations_used_this_month=0) if plan_features.name.lower() == 'free' else None
        )

    def from_odoo_plan_product_to_features(self, odoo_product_data: Optional[Dict[str, Any]]) -> PlanFeatures:
        """Maps an Odoo product.template dictionary to our PlanFeatures model."""
        # This assumes Odoo product templates have custom boolean fields like 'x_unlimited_generations'
        if not odoo_product_data:
            return PlanFeatures(name="Unknown Plan") # Fallback
            
        return PlanFeatures(
            name=odoo_product_data.get('name', 'Unnamed Plan'),
            price_monthly=Decimal(odoo_product_data.get('list_price', '0.0')),
            unlimited_standard_generations=odoo_product_data.get('x_unlimited_generations', False),
            brand_kit_access=odoo_product_data.get('x_brand_kit_access', False),
            hd_exports=odoo_product_data.get('x_hd_exports', False),
            priority_support=odoo_product_data.get('x_priority_support', False),
            collaboration_tools=odoo_product_data.get('x_collaboration_tools', False),
            # ... and so on for all feature flags
        )

    def from_odoo_credit_balance_to_domain(self, user_id: UUID, balance_value: float) -> CreditBalanceDomain:
        """Maps a raw credit balance value from Odoo to our domain model."""
        return CreditBalanceDomain(
            user_id=user_id,
            balance=Decimal(balance_value),
            last_updated_at=datetime.utcnow() # Timestamp the mapping time
        )
        
    def from_odoo_invoice_to_summary(self, odoo_invoice: Dict[str, Any]) -> Dict:
        """Maps an Odoo account.move dictionary to a simplified summary dictionary for the API."""
        return {
            "invoice_id": odoo_invoice.get("name"),
            "date": odoo_invoice.get("invoice_date"),
            "total_amount": Decimal(odoo_invoice.get("amount_total", 0.0)),
            "status": odoo_invoice.get("payment_state"),
            "pdf_url": odoo_invoice.get("access_url") # Odoo portal link to view/download
        }

    def to_odoo_tax_calc_details(self, user_id: UUID, purchase_details: Dict) -> Dict:
        """Maps purchase preview details from our API to a format Odoo's tax calculator might expect."""
        # This is highly conceptual and depends on the custom Odoo method.
        return {
            "user_cf_id": str(user_id),
            "order_lines": purchase_details.get("items", []), # e.g., [{"product_id": 123, "quantity": 1}]
            "customer_address": purchase_details.get("customer_address", {})
        }

    def from_odoo_tax_calc_to_domain(self, odoo_tax_data: Dict[str, Any]) -> Dict:
        """Maps the result from Odoo's tax calculation back to our API schema format."""
        return {
            "subtotal": Decimal(odoo_tax_data.get("amount_untaxed", 0.0)),
            "tax_amount": Decimal(odoo_tax_data.get("amount_tax", 0.0)),
            "total_amount": Decimal(odoo_tax_data.get("amount_total", 0.0)),
            "tax_breakdown": odoo_tax_data.get("tax_lines_data", []) # Expects a list of dicts from Odoo
        }

    def _map_odoo_stage_to_status(self, stage_name: str) -> SubscriptionStatus:
        """Helper to map Odoo's text-based stage names to our enum."""
        stage_map = {
            "in progress": SubscriptionStatus.ACTIVE,
            "draft": SubscriptionStatus.TRIAL, # Example mapping
            "to renew": SubscriptionStatus.ACTIVE,
            "closed": SubscriptionStatus.EXPIRED,
            "cancelled": SubscriptionStatus.CANCELLED
        }
        return stage_map.get(stage_name.lower(), SubscriptionStatus.CANCELLED)

    def _get_default_free_plan(self, user_id: UUID) -> UserSubscriptionDomain:
        """Returns a default UserSubscriptionDomain object for a user on the Free plan."""
        features = PlanFeatures(name="Free") # Minimal features
        return UserSubscriptionDomain(
            user_id=user_id,
            current_plan_id="free_plan",
            current_plan_name="Free",
            status=SubscriptionStatus.ACTIVE,
            features=features,
            freemium_limits=FreemiumLimits(generations_used_this_month=0) # Placeholder usage
        )