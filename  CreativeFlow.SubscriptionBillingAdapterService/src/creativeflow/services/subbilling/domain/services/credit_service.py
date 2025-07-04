import logging
from uuid import UUID
from typing import Optional, Dict
from decimal import Decimal, ROUND_UP

from ..models.credit_models import CreditBalanceDomain, CreditCost
from ...infrastructure.odoo_client import OdooClient
from ...infrastructure.db.repositories.user_repository import UserRepository
from .odoo_mapping_service import OdooMappingService
from .subscription_service import SubscriptionService
from ...infrastructure.odoo_client import OdooRPCError

logger = logging.getLogger(__name__)

class InsufficientCreditsError(Exception):
    """Custom exception for when a user does not have enough credits."""
    def __init__(self, message, required: Decimal, balance: Decimal):
        super().__init__(message)
        self.required = required
        self.balance = balance

class CreditService:
    """
    Contains the business logic for managing user credits.
    """
    
    # Credit costs as per REQ-016. Using Decimal for precision.
    CREDIT_COSTS: Dict[str, Decimal] = {
        "sample_generation": Decimal("0.25"),
        "standard_generation": Decimal("1.00"),
        "hd_export": Decimal("2.00"),
        # 'advanced_ai_feature' cost is variable and determined by parameters.
    }

    def __init__(
        self,
        odoo_client: OdooClient,
        user_repo: UserRepository,
        odoo_map_service: OdooMappingService,
        subscription_service: SubscriptionService
    ):
        self.odoo_client = odoo_client
        self.user_repo = user_repo
        self.odoo_map_service = odoo_map_service
        self.subscription_service = subscription_service

    async def get_user_credit_balance(self, user_id: UUID) -> CreditBalanceDomain:
        """Retrieves a user's current credit balance from Odoo."""
        logger.info(f"Fetching credit balance for user {user_id}")
        try:
            balance_val = self.odoo_client.get_credit_balance(str(user_id))
            return self.odoo_map_service.from_odoo_credit_balance_to_domain(user_id, balance_val)
        except OdooRPCError as e:
            logger.error(f"Odoo RPC Error fetching credit balance for user {user_id}: {e}", exc_info=True)
            raise

    async def get_credit_cost_for_action(self, user_id: UUID, action_type: str, advanced_params: Optional[Dict] = None) -> Decimal:
        """
        Calculates the credit cost for a given action, considering the user's plan.
        """
        subscription = await self.subscription_service.get_user_subscription_status(user_id)
        
        # REQ-016: Pro plan has unlimited standard generations
        if subscription.features.unlimited_standard_generations and action_type in ["sample_generation", "standard_generation"]:
            return Decimal("0.00")
            
        if action_type == "advanced_ai_feature":
            # REQ-016: Dynamic pricing for advanced features
            # The logic here would parse `advanced_params` to determine the cost.
            # For example, cost could be based on resolution, steps, etc.
            # This logic might even involve another call to Odoo to get a price quote.
            base_cost = advanced_params.get("base_cost", 5.0) if advanced_params else 5.0
            return Decimal(base_cost).quantize(Decimal("0.01"), rounding=ROUND_UP)

        return self.CREDIT_COSTS.get(action_type, Decimal("0.00"))

    async def check_sufficient_credits(self, user_id: UUID, action_type: str, advanced_params: Optional[Dict] = None) -> bool:
        """Checks if the user has enough credits for a specific action."""
        cost = await self.get_credit_cost_for_action(user_id, action_type, advanced_params)
        if cost == Decimal("0.00"):
            return True
            
        balance = await self.get_user_credit_balance(user_id)
        return balance.balance >= cost

    async def deduct_credits_for_action(
        self,
        user_id: UUID,
        action_type: str,
        reference_id: Optional[str] = None,
        advanced_params: Optional[Dict] = None
    ) -> bool:
        """
        Deducts credits for an action after verifying the balance.
        Raises InsufficientCreditsError if the balance is too low.
        """
        cost = await self.get_credit_cost_for_action(user_id, action_type, advanced_params)
        logger.info(f"Deducting credits for user {user_id}, action '{action_type}', cost {cost}")

        if cost <= 0:
            logger.info(f"Action '{action_type}' has no cost for user {user_id}. No deduction needed.")
            return True

        balance_domain = await self.get_user_credit_balance(user_id)
        if balance_domain.balance < cost:
            logger.warning(f"Insufficient credits for user {user_id}. Required: {cost}, Balance: {balance_domain.balance}")
            raise InsufficientCreditsError(
                "User has insufficient credits for this action.",
                required=cost,
                balance=balance_domain.balance
            )

        try:
            success = self.odoo_client.deduct_credits(str(user_id), float(cost), action_type, reference_id)
            if success:
                logger.info(f"Successfully deducted {cost} credits from user {user_id}")
            else:
                logger.error(f"Odoo reported failure in deducting credits for user {user_id}")
            return success
        except OdooRPCError as e:
            logger.error(f"Odoo RPC Error deducting credits for user {user_id}: {e}", exc_info=True)
            return False

    async def refund_credits_for_system_error(
        self,
        user_id: UUID,
        amount: Decimal,
        original_action_id: str,
        reason: str
    ) -> bool:
        """
        Adds credits to a user's account, e.g., for a refund due to a system error.
        """
        logger.info(f"Refunding {amount} credits to user {user_id} for action {original_action_id}. Reason: {reason}")
        if amount <= 0:
            return True

        try:
            success = self.odoo_client.add_credits(
                user_id_cf=str(user_id),
                amount=float(amount),
                reason=reason,
                reference_id=original_action_id
            )
            if success:
                 logger.info(f"Successfully refunded {amount} credits to user {user_id}")
            else:
                logger.error(f"Odoo reported failure in refunding credits for user {user_id}")
            return success
        except OdooRPCError as e:
            logger.error(f"Odoo RPC Error refunding credits for user {user_id}: {e}", exc_info=True)
            return False