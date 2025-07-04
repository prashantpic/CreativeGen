import logging
import xmlrpc.client
from functools import partial
import asyncio

logger = logging.getLogger(__name__)

class OdooAdapterClient:
    """
    Client for interacting with Odoo backend via XML-RPC.
    
    NOTE: xmlrpc.client is synchronous. To avoid blocking the asyncio event loop,
    its calls are wrapped to run in a thread pool executor.
    """
    def __init__(self, url: str, db: str, uid: int, password: str):
        self.url = url
        self.db = db
        self.uid = uid
        self.password = password
        self.common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
        self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')
        
        # Check connection and authenticate on init, though this is a sync call
        try:
            version = self.common.version()
            logger.info(f"Successfully connected to Odoo version: {version}")
        except Exception as e:
            logger.error(f"Failed to connect to Odoo at {self.url}: {e}")
            # In a real app, you might want to raise this or handle it more gracefully
            
    async def _execute_kw_async(self, model: str, method: str, args: list, kwargs: dict = None):
        """
        Executes an Odoo RPC method asynchronously by running the synchronous
        call in a separate thread.
        """
        loop = asyncio.get_running_loop()
        
        # Prepare the synchronous call using functools.partial
        sync_call = partial(
            self.models.execute_kw,
            self.db,
            self.uid,
            self.password,
            model,
            method,
            args,
            kwargs or {}
        )
        
        try:
            # Run the synchronous call in the default thread pool executor
            result = await loop.run_in_executor(None, sync_call)
            return result
        except Exception as e:
            logger.error(f"Odoo RPC call failed for model '{model}', method '{method}': {e}", exc_info=True)
            # Depending on requirements, you might want to re-raise a custom exception
            raise ConnectionError(f"Odoo RPC call failed: {e}") from e

    async def call_odoo_rpc(self, model: str, method: str, args: list, kwargs: dict = None) -> any:
        """
        Generic method to call an Odoo RPC endpoint.

        Args:
            model (str): The Odoo model name (e.g., 'res.partner').
            method (str): The method to call on the model (e.g., 'search_read').
            args (list): A list of positional arguments for the method.
            kwargs (dict, optional): A dictionary of keyword arguments.

        Returns:
            Any: The result from the Odoo RPC call.
        """
        logger.debug(f"Calling Odoo RPC: model={model}, method={method}, args={args}, kwargs={kwargs}")
        return await self._execute_kw_async(model, method, args, kwargs)

    # Example specific methods (can be used by a higher-level credit service if Odoo is the backend)
    async def validate_user_subscription_and_credits(self, user_id: str, required_credits: float) -> tuple[bool, str]:
        """
        Example method to validate subscription and credits directly from Odoo.
        The actual implementation would depend heavily on the Odoo model structure.
        """
        # This is a placeholder for the actual Odoo logic
        logger.info(f"Calling Odoo to validate credits for user {user_id}")
        
        # Example: Find the partner/user record
        partner_id = await self.call_odoo_rpc(
            'res.partner', 'search', [[('x_user_id', '=', user_id)]], {'limit': 1}
        )
        
        if not partner_id:
            return False, "User not found in Odoo"
            
        # Example: Read their credit balance and subscription status
        partner_data = await self.call_odoo_rpc(
            'res.partner', 'read', [partner_id], {'fields': ['x_credit_balance', 'x_subscription_status']}
        )
        
        if not partner_data:
            return False, "Could not read user data from Odoo"
        
        data = partner_data[0]
        if data.get('x_subscription_status') != 'active':
            return False, f"Subscription is not active ({data.get('x_subscription_status')})"
        
        if data.get('x_credit_balance', 0) < required_credits:
            return False, f"Insufficient credits. Have: {data.get('x_credit_balance')}, Need: {required_credits}"
            
        return True, "Validation successful"