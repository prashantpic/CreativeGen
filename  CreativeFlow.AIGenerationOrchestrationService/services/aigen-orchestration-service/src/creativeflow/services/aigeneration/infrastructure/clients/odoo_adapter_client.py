import logging
from typing import Any, Tuple, List, Dict
from uuid import UUID
import xmlrpc.client
import asyncio

logger = logging.getLogger(__name__)

# This client uses the standard xmlrpc.client library. Its methods are blocking.
# To use it in an async application, these blocking calls should be wrapped
# in `asyncio.to_thread()` as shown in the public methods.

class OdooAdapterClient:
    """
    Client adapter for interacting with the Odoo backend for billing/credit operations.
    Acts as an adapter to the Odoo system for functionalities related to user credits,
    subscriptions, and potentially triggering Odoo-side updates post-generation.
    """
    def __init__(self, url: str, db: str, uid: int, password: str):
        self._odoo_url = url
        self._odoo_db = db
        self._odoo_uid = uid
        self._odoo_password = password
        logger.info(f"OdooAdapterClient initialized for URL: {self._odoo_url} and DB: {self._odoo_db}")

    def _get_proxy(self, model: str) -> xmlrpc.client.ServerProxy:
        """Helper to get a server proxy for a specific Odoo model."""
        common_proxy = xmlrpc.client.ServerProxy(f'{self._odoo_url}/xmlrpc/2/common')
        # Here we would authenticate, but for this client, we assume uid/password is passed to each call.
        # This proxy is for the object endpoint
        return xmlrpc.client.ServerProxy(f'{self._odoo_url}/xmlrpc/2/object')

    def _execute_kw(self, model: str, method: str, args: list, kwargs: dict = None) -> Any:
        """
        Private blocking method to execute a command on an Odoo model.
        This is the method that will be run in a separate thread.
        """
        if kwargs is None:
            kwargs = {}
        proxy = self._get_proxy(model)
        try:
            logger.debug(f"Executing Odoo RPC: model='{model}', method='{method}', args='{args}', kwargs='{kwargs}'")
            result = proxy.execute_kw(self._odoo_db, self._odoo_uid, self._odoo_password, model, method, args, kwargs)
            logger.debug(f"Odoo RPC call successful. Result: {result}")
            return result
        except xmlrpc.client.Fault as e:
            logger.error(f"Odoo RPC Fault: {e.faultString}", exc_info=True)
            raise ConnectionError(f"Odoo RPC Error: {e.faultString}")
        except Exception as e:
            logger.error(f"An unexpected error occurred during Odoo RPC call: {e}", exc_info=True)
            raise ConnectionError(f"Failed to communicate with Odoo: {e}")

    async def call_odoo_rpc(self, model: str, method: str, args: List, kwargs: Dict = None) -> Any:
        """
        Asynchronously calls a generic Odoo RPC method.
        """
        return await asyncio.to_thread(self._execute_kw, model, method, args, kwargs)

    async def validate_user_subscription_and_credits(self, user_id: str, required_credits: float) -> Tuple[bool, str]:
        """
        Example of a specific business logic method.
        Calls a custom method on a custom Odoo model.
        Returns (isValid, reason_if_not_valid)
        """
        # This assumes a custom model 'creative.user.credit' and method 'validate_generation_request' exists in Odoo.
        model = "creative.user.credit"
        method = "validate_generation_request"
        args = [[user_id], required_credits] # Odoo often expects search domains in lists
        
        try:
            result = await self.call_odoo_rpc(model, method, args)
            # Assuming Odoo returns a tuple like (True, "Success") or (False, "Insufficient Credits")
            if isinstance(result, (list, tuple)) and len(result) == 2:
                is_valid, reason = result
                return bool(is_valid), str(reason)
            logger.warning(f"Unexpected response format from Odoo validation: {result}")
            return False, "Invalid response from Odoo"
        except ConnectionError as e:
            return False, str(e)

    async def deduct_user_credits(self, user_id: str, generation_request_id: UUID, credits_to_deduct: float, action_description: str) -> bool:
        """
        Instructs Odoo to deduct credits for a generation.
        """
        model = "creative.user.credit"
        method = "deduct_credits_for_generation"
        args = []
        kwargs = {
            'user_id': user_id,
            'request_id': str(generation_request_id),
            'amount': credits_to_deduct,
            'description': action_description
        }
        try:
            result = await self.call_odoo_rpc(model, method, args, kwargs)
            # Assuming Odoo returns True on success
            return bool(result)
        except ConnectionError:
            return False

    async def refund_user_credits(self, user_id: str, generation_request_id: UUID, credits_to_refund: float, reason: str) -> bool:
        """
        Requests a credit refund from Odoo in case of system errors.
        """
        model = "creative.user.credit"
        method = "refund_credits_for_generation"
        args = []
        kwargs = {
            'user_id': user_id,
            'request_id': str(generation_request_id),
            'amount': credits_to_refund,
            'reason': reason
        }
        try:
            result = await self.call_odoo_rpc(model, method, args, kwargs)
            # Assuming Odoo returns True on success
            return bool(result)
        except ConnectionError:
            return False