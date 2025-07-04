import logging
import asyncio
from typing import Any, List, Dict
import xmlrpc.client

logger = logging.getLogger(__name__)

class OdooAdapterClient:
    """
    Client for interacting with an Odoo backend via XML-RPC.

    Note: The standard `xmlrpc.client` is synchronous. In a fully async
    application, these calls should be wrapped with `asyncio.to_thread`
    to avoid blocking the event loop.
    """

    def __init__(self, url: str, db: str, uid: int, password: str):
        self.url = url
        self.db = db
        self.uid = uid
        self.password = password
        self.common_proxy = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
        self.object_proxy = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')

    def _authenticate(self) -> int:
        """Authenticates with Odoo and returns the user ID."""
        try:
            uid = self.common_proxy.authenticate(self.db, self.uid, self.password, {})
            if not uid:
                raise ConnectionRefusedError("Odoo authentication failed. Check credentials.")
            return uid
        except Exception as e:
            logger.error(f"Odoo authentication failed: {e}")
            raise ConnectionRefusedError(f"Odoo authentication failed: {e}")


    async def call_odoo_rpc(
        self,
        model: str,
        method: str,
        args: List[Any],
        kwargs: Dict[str, Any] = None
    ) -> Any:
        """
        Generic method to make an asynchronous RPC call to Odoo.

        Wraps the synchronous `xmlrpc.client` call in a separate thread.
        """
        if kwargs is None:
            kwargs = {}
            
        def _execute_rpc():
            # The authentication step might be redundant if the UID/password is for a technical user
            # and is always valid. However, it's good practice.
            # uid = self._authenticate()
            # For simplicity, we'll use the pre-configured UID.
            return self.object_proxy.execute_kw(
                self.db, self.uid, self.password, model, method, args, kwargs
            )
        
        try:
            logger.debug(f"Calling Odoo RPC: model={model}, method={method}")
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(None, _execute_rpc)
            logger.debug(f"Odoo RPC call successful: model={model}, method={method}")
            return result
        except Exception as e:
            logger.error(f"Error calling Odoo RPC: model={model}, method={method}. Error: {e}", exc_info=True)
            # Depending on the desired behavior, you might want to raise a custom exception here.
            raise

    # --- Example Specific Methods ---
    # These would be called by the CreditServiceClient if it were an adapter for Odoo.
    
    async def validate_user_subscription_and_credits(self, user_id: str, required_credits: float) -> tuple[bool, str]:
        """
        Example of a specific business logic call to Odoo.
        Returns (isValid, reason_if_not_valid)
        """
        args = [[('external_user_id', '=', user_id)], required_credits]
        result = await self.call_odoo_rpc(
            model='res.partner',
            method='check_credits_and_subscription_api',
            args=args
        )
        if isinstance(result, dict) and 'is_valid' in result:
             return result.get('is_valid', False), result.get('reason', 'Unknown error')
        return False, "Invalid response from Odoo"

    async def deduct_user_credits(self, user_id: str, generation_request_id: str, credits_to_deduct: float, action_description: str) -> bool:
        """Example of a credit deduction call to Odoo."""
        args = [user_id, str(generation_request_id), credits_to_deduct, action_description]
        result = await self.call_odoo_rpc(
            model='res.partner',
            method='deduct_credits_api',
            args=args
        )
        return bool(result)

    async def refund_user_credits(self, user_id: str, generation_request_id: str, credits_to_refund: float, reason: str) -> bool:
        """Example of a credit refund call to Odoo."""
        args = [user_id, str(generation_request_id), credits_to_refund, reason]
        result = await self.call_odoo_rpc(
            model='res.partner',
            method='refund_credits_api',
            args=args
        )
        return bool(result)