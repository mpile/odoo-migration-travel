# core/rpc_client.py
import xmlrpc.client
import logging

logger = logging.getLogger(__name__)

class OdooRPCClient:
    def __init__(self, config):
        self.config = config
        self.models = None
        self.uid = None
        self.connect()
    
    def connect(self):
        try:
            common = xmlrpc.client.ServerProxy(f"{self.config['url']}/xmlrpc/2/common")
            self.uid = common.authenticate(
                self.config['db'], 
                self.config['username'], 
                self.config['password'], 
                {}
            )
            self.models = xmlrpc.client.ServerProxy(f"{self.config['url']}/xmlrpc/2/object")
            logger.info("✅ Connected to Odoo")
        except Exception as e:
            logger.error(f"❌ Connection failed: {e}")
            raise
