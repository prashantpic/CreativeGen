import logging
from typing import Optional, Dict, List, Any
import odoorpc
from ..core.config import Settings

# Set up logger
logger = logging.getLogger(__name__)

class OdooConnectionError(Exception):
    """Custom exception for failures in connecting to Odoo."""
    pass

class OdooRPCError(Exception):
    """Custom exception for errors returned by Odoo RPC calls."""
    def __init__(self, message, odoo_fault_code=None, odoo_fault_string=None):
        super().__init__(message)
        self.odoo_fault_code = odoo_fault_code
        self.odoo_fault_string = odoo_fault_string

class OdooClient:
    """
    A client for interacting with the Odoo ERP system via JSON-RPC.
    This class abstracts all Odoo-specific communication.
    """

    def __init__(self, config: Settings):
        self.config = config
        self.odoo: Optional[odoorpc.ODOO] = None
        self._connect()

    def _connect(self):
        """Establishes and authenticates a connection to the Odoo instance."""
        logger.info(f"Attempting to connect to Odoo at {self.config.ODOO_URL}...")
        try:
            # Assuming the port is part of the ODOO_URL if not standard
            self.odoo = odoorpc.ODOO(self.config.ODOO_URL, protocol='jsonrpc')
            self.odoo.login(
                self.config.ODOO_DB,
                self.config.ODOO_USERNAME,
                self.config.ODOO_PASSWORD.get_secret_value()
            )
            logger.info("Successfully connected and logged into Odoo.")
        except (odoorpc.error.RPCError, odoorpc.error.ConnectionError) as e:
            logger.error(f"Failed to connect or login to Odoo: {e}", exc_info=True)
            self.odoo = None
            raise OdooConnectionError(f"Could not connect to Odoo: {e}")

    def _ensure_connection(self):
        """Ensures the Odoo client is connected, reconnecting if necessary."""
        try:
            # A lightweight check to see if the connection is alive.
            if self.odoo is None or not self.odoo.env:
                logger.warning("Odoo connection lost or not initialized. Reconnecting...")
                self._connect()
        except Exception:
            logger.warning("Odoo connection check failed. Reconnecting...")
            self._connect()

    def _execute_kw(self, model: str, method: str, args: List[Any], kwargs: Optional[Dict[str, Any]] = None) -> Any:
        """
        A private helper to wrap `execute_kw` with error handling and connection checks.
        
        Args:
            model: The Odoo model name (e.g., 'res.partner').
            method: The method to call on the model (e.g., 'search_read').
            args: A list of positional arguments for the Odoo method.
            kwargs: A dictionary of keyword arguments for the Odoo method.
        
        Returns:
            The result from the Odoo RPC call.
        
        Raises:
            OdooRPCError: If the Odoo call results in an error.
        """
        self._ensure_connection()
        kwargs = kwargs or {}
        logger.debug(f"Executing Odoo call: model='{model}', method='{method}', args='{args}', kwargs='{kwargs}'")
        try:
            return self.odoo.execute_kw(model, method, args, kwargs)
        except odoorpc.error.RPCError as e:
            logger.error(f"Odoo RPC error on model '{model}', method '{method}': {e}", exc_info=True)
            raise OdooRPCError(
                message=f"Odoo error calling {model}.{method}: {e.faultString}",
                odoo_fault_code=e.faultCode,
                odoo_fault_string=e.faultString
            ) from e

    # --- Subscription Methods ---
    # Note: Odoo model/method names are examples and depend on Odoo customization.
    
    def get_current_user_plan_info(self, user_id_cf: str) -> Optional[Dict]:
        partner_id = self._find_partner_by_cf_id(user_id_cf)
        if not partner_id:
            return None
        
        domain = [('partner_id', '=', partner_id), ('stage_category', '=', 'progress')]
        fields = ['name', 'code', 'stage_id', 'date_start', 'recurring_next_date', 'template_id']
        subscriptions = self._execute_kw('sale.subscription', 'search_read', [domain], {'fields': fields, 'limit': 1})
        return subscriptions[0] if subscriptions else None

    def update_subscription(self, user_id_cf: str, new_plan_odoo_id: int, action: str) -> Dict:
        # This is a conceptual implementation. The actual Odoo method might be a single
        # custom method that handles all these actions.
        # e.g., self.env['res.partner'].browse(id).update_subscription(...)
        partner_id = self._find_partner_by_cf_id(user_id_cf)
        if not partner_id:
            raise ValueError("User not found in Odoo")
            
        args = [partner_id, new_plan_odoo_id, action]
        # Assuming a custom method `creativeflow_update_subscription` on `res.partner`
        result = self._execute_kw('res.partner', 'creativeflow_update_subscription', args)
        return result

    # --- Credit Methods ---
    
    def get_credit_balance(self, user_id_cf: str) -> float:
        partner_id = self._find_partner_by_cf_id(user_id_cf)
        if not partner_id:
            return 0.0
        
        # Assuming a custom field 'x_credit_balance' on 'res.partner'
        partner_data = self._execute_kw('res.partner', 'read', [[partner_id]], {'fields': ['x_credit_balance']})
        return partner_data[0].get('x_credit_balance', 0.0) if partner_data else 0.0

    def deduct_credits(self, user_id_cf: str, amount: float, reason: str, reference_id: Optional[str] = None) -> bool:
        partner_id = self._find_partner_by_cf_id(user_id_cf)
        if not partner_id:
            raise ValueError("User not found in Odoo")
            
        # Assuming a custom method `creativeflow_deduct_credits` on `res.partner`
        # This method in Odoo would handle the transaction logging and balance update atomically.
        kwargs = {'amount': amount, 'reason': reason, 'reference_id': reference_id}
        result = self._execute_kw('res.partner', 'creativeflow_deduct_credits', [partner_id], kwargs)
        return result.get('success', False)

    def add_credits(self, user_id_cf: str, amount: float, reason: str, reference_id: Optional[str] = None) -> bool:
        partner_id = self._find_partner_by_cf_id(user_id_cf)
        if not partner_id:
            raise ValueError("User not found in Odoo")
            
        # Assuming a custom method `creativeflow_add_credits` on `res.partner`
        kwargs = {'amount': amount, 'reason': reason, 'reference_id': reference_id}
        result = self._execute_kw('res.partner', 'creativeflow_add_credits', [partner_id], kwargs)
        return result.get('success', False)

    # --- Billing/Invoice/Tax Methods ---

    def get_invoices_for_user(self, user_id_cf: str, limit: int = 10) -> List[Dict]:
        partner_id = self._find_partner_by_cf_id(user_id_cf)
        if not partner_id:
            return []
            
        domain = [('partner_id', '=', partner_id), ('move_type', '=', 'out_invoice')]
        fields = ['name', 'invoice_date', 'amount_total', 'payment_state', 'access_url']
        order = 'invoice_date desc'
        invoices = self._execute_kw('account.move', 'search_read', [domain], {'fields': fields, 'limit': limit, 'order': order})
        return invoices

    def get_payment_portal_link_for_user(self, user_id_cf: str) -> Optional[str]:
        # This highly depends on Odoo's portal setup. Odoo's portal provides a generic
        # home URL that can be constructed or fetched.
        partner_id = self._find_partner_by_cf_id(user_id_cf)
        if not partner_id:
            return None
        # This is a conceptual call; the real method may differ.
        try:
            portal_url = self._execute_kw('res.partner', 'get_portal_url', [[partner_id]])
            return portal_url
        except OdooRPCError:
            logger.warning(f"Could not retrieve a specific portal URL for user {user_id_cf}")
            return f"{self.config.ODOO_URL}/my/home" # Fallback to a generic portal URL

    # --- Helper Methods ---

    def _find_partner_by_cf_id(self, user_id_cf: str) -> Optional[int]:
        """Finds an Odoo res.partner ID based on our platform's user ID."""
        # Assumes a custom field 'x_creativeflow_user_id' on 'res.partner' for mapping.
        domain = [('x_creativeflow_user_id', '=', user_id_cf)]
        partner_ids = self._execute_kw('res.partner', 'search', [domain], {'limit': 1})
        if not partner_ids:
            logger.warning(f"No Odoo partner found for CreativeFlow user ID '{user_id_cf}'")
            return None
        return partner_ids[0]

    # --- Other conceptual methods from SDS (as placeholders) ---

    def trigger_invoice_generation_for_subscription(self, subscription_odoo_id: int) -> str:
        # Conceptual: This would call Odoo's logic to generate a recurring invoice.
        # e.g., self.env['sale.subscription'].browse(id)._create_invoice()
        result = self._execute_kw('sale.subscription', 'action_subscription_invoice', [[subscription_odoo_id]])
        # The result might be an action dictionary or the ID of the new invoice.
        # This needs to be aligned with the actual Odoo implementation.
        return str(result.get('invoice_id', ''))

    def calculate_tax_for_order(self, order_details: dict) -> dict:
        # Conceptual: This would likely involve creating a temporary sales order and
        # reading the calculated tax lines.
        # Odoo's tax calculation is complex and tied to fiscal positions, products, and partners.
        result = self._execute_kw('sale.order', 'creativeflow_calculate_tax', [order_details])
        return result

    def process_dunning_notification(self, subscription_odoo_id: int, failure_reason: str) -> dict:
        # Conceptual: Call a method on the subscription to trigger the dunning process.
        result = self._execute_kw(
            'sale.subscription', 
            'creativeflow_process_dunning', 
            [[subscription_odoo_id]], 
            {'failure_reason': failure_reason}
        )
        return result