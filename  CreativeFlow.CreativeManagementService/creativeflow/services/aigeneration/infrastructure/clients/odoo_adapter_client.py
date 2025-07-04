import logging
import xmlrpc.client
from functools import partial
import asyncio

logger = logging.getLogger(__name__)

class OdooAdapterClient:
    """
    Client for interacting with an Odoo backend via XML-RPC.
    
    Note: The standard `xmlrpc.client` is synchronous. To avoid blocking the
    asyncio event loop, RPC calls are wrapped in `loop.run_in_executor`.
    A truly async RPC library would be a better fit for a fully async application.
    """
    def __init__(self, url: str, db: str, uid: int, password: str):
        self.url = url
        self.db = db
        self.uid = uid
        self.password = password

    async def _execute_rpc(self, model: str, method: str, args: list, kwargs: dict = None):
        """
        Executes an Odoo RPC call in a separate thread to avoid blocking.
        """
        loop = asyncio.get_running_loop()
        try:
            # Create a partial function to be executed in the thread pool
            rpc_call = partial(
                self._sync_execute, 
                model, 
                method, 
                args, 
                kwargs or {}
            )
            result = await loop.run_in_executor(None, rpc_call)
            return result
        except Exception as e:
            logger.error(f"Odoo RPC call failed for model '{model}', method '{method}': {e}", exc_info=True)
            raise

    def _sync_execute(self, model, method, args, kwargs):
        """The synchronous part of the RPC call that runs in the executor."""
        common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
        # Here we re-authenticate for each call. In a high-traffic scenario,
        # you might explore session management if the Odoo API supports it.
        uid = common.authenticate(self.db, self.uid, self.password, {})
        if not uid:
             raise ConnectionRefusedError("Odoo authentication failed.")
        
        object_proxy = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')
        return object_proxy.execute_kw(self.db, uid, self.password, model, method, args, kwargs)

    async def call_odoo_rpc(self, model: str, method: str, args: list, kwargs: dict = None):
        """
        Generic method to call any Odoo 'execute_kw' RPC method.

        :param model: The Odoo model name (e.g., 'res.partner').
        :param method: The method to call on the model (e.g., 'search_read').
        :param args: A list of positional arguments for the RPC method.
        :param kwargs: A dict of keyword arguments for the RPC method.
        :return: The result of the RPC call.
        """
        logger.debug(f"Calling Odoo RPC: model={model}, method={method}")
        return await self._execute_rpc(model, method, args, kwargs)

    # Example of a specific method built on top of the generic one
    async def validate_user_subscription_and_credits(self, user_id: str, required_credits: float) -> tuple[bool, str]:
        """
        Example method to validate user subscription and credits directly via Odoo.
        This logic would typically live in the dedicated Credit Service.
        """
        # This is a hypothetical implementation. The actual model and method names would
        # depend on the custom Odoo implementation for CreativeFlow.
        res = await self.call_odoo_rpc(
            model='creativeflow.user.profile',
            method='check_generation_credits',
            args=[[int(user_id)]],  # Odoo often expects IDs in a list
            kwargs={'required_credits': required_credits}
        )
        # Assuming the Odoo method returns a tuple like (True, "Sufficient credits")
        if isinstance(res, (list, tuple)) and len(res) == 2:
            return res[0], res[1]
        
        logger.error(f"Unexpected response from Odoo credit check: {res}")
        return False, "Failed to validate credits due to an internal error."