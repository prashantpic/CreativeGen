import logging
from typing import Any, List, Dict
import xmlrpc.client
import asyncio

logger = logging.getLogger(__name__)

class OdooAdapterClient:
    """
    Client for interacting with an Odoo instance via XML-RPC.
    
    Note: The standard `xmlrpc.client` is blocking. To use it in an async
    application without blocking the event loop, its calls should be run
    in a separate thread pool using `asyncio.to_thread`.
    """

    def __init__(self, url: str, db: str, uid: int, password: str):
        self.url = url
        self.db = db
        self.uid = uid
        self.password = password
        self.common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
        self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')
        
        # A simple check on initialization
        try:
            version = self.common.version()
            logger.info(f"Successfully connected to Odoo version: {version['server_version']}")
        except Exception as e:
            logger.error(f"Failed to connect to Odoo at {self.url}. Error: {e}")
            # Depending on requirements, could raise an exception to halt startup
            # raise ConnectionError(f"Could not connect to Odoo: {e}")

    def _execute_kw(self, model: str, method: str, args: List, kwargs: Dict) -> Any:
        """
        Private synchronous method to execute a model method in Odoo.
        """
        try:
            return self.models.execute_kw(
                self.db, self.uid, self.password, model, method, args, kwargs
            )
        except xmlrpc.client.Fault as e:
            logger.error(f"Odoo RPC Fault: Model={model}, Method={method}, Error={e.faultString}")
            raise  # Re-raise to be handled by the calling async method
        except Exception as e:
            logger.error(f"Odoo RPC Error: Model={model}, Method={method}, Error={e}", exc_info=True)
            raise

    async def call_odoo_rpc(self, model: str, method: str, args: list, kwargs: dict = None) -> Any:
        """
        Asynchronously calls an Odoo model method using a thread pool.
        This is a generic method for interacting with Odoo.

        :param model: The name of the Odoo model (e.g., 'res.partner').
        :param method: The name of the method to call on the model (e.g., 'search_read').
        :param args: A list of positional arguments for the method.
        :param kwargs: A dictionary of keyword arguments for the method.
        :return: The result from the Odoo RPC call.
        """
        if kwargs is None:
            kwargs = {}
            
        logger.debug(f"Executing Odoo RPC call: model='{model}', method='{method}'")
        
        # Run the blocking xmlrpc call in a separate thread
        try:
            result = await asyncio.to_thread(self._execute_kw, model, method, args, kwargs)
            logger.debug(f"Odoo RPC call successful: model='{model}', method='{method}'")
            return result
        except Exception as e:
            logger.error(f"Odoo RPC call failed: model='{model}', method='{method}'. Error: {e}")
            # Propagate the exception to be handled by the service layer
            raise ConnectionError(f"Failed to execute Odoo RPC call: {e}") from e

    # Example of a specific method, although the generic one is often sufficient
    async def validate_user_subscription_and_credits(self, user_id: str, required_credits: float) -> dict:
        """
        A specific example method to call a custom Odoo model method.
        """
        model = 'creative.user' # Example custom model in Odoo
        method = 'check_credits_and_subscription'
        args = [[int(user_id)]] # Odoo often expects IDs in a list
        kwargs = {'required_credits': required_credits}
        
        # This assumes the Odoo method returns a dict like {'valid': bool, 'reason': str}
        return await self.call_odoo_rpc(model, method, args, kwargs)