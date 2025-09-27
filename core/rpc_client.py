# core/rpc_client.py
import xmlrpc.client
import logging
import pymysql
from config.settings import MYSQL_CONFIG

logger = logging.getLogger(__name__)

class OdooRPCClient:
    def __init__(self, config):
        self.config = config
        self.models = None
        self.uid = None
        self.mysql_conn = None
        self.mysql_cursor = None
        self.connect_odoo()
        self.connect_mysql()
    
    def connect_odoo(self):
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
            logger.error(f"❌ Odoo connection failed: {e}")
            raise
    
    def connect_mysql(self):
        try:
            self.mysql_conn = pymysql.connect(**MYSQL_CONFIG)
            self.mysql_cursor = self.mysql_conn.cursor()
            logger.info("✅ Connected to MySQL")
        except Exception as e:
            logger.error(f"❌ MySQL connection failed: {e}")
            raise
    
    def search_record(self, model, domain):
        try:
            return self.models.execute_kw(
                self.config['db'], self.uid, self.config['password'],
                model, 'search', [domain]
            )
        except Exception as e:
            logger.error(f"Search error in {model}: {e}")
            return []
    
    def create_record(self, model, values):
        try:
            return self.models.execute_kw(
                self.config['db'], self.uid, self.config['password'],
                model, 'create', [values]
            )
        except Exception as e:
            logger.error(f"Create error in {model}: {e}")
            return False
    
    def close(self):
        if self.mysql_cursor:
            self.mysql_cursor.close()
        if self.mysql_conn:
            self.mysql_conn.close()
        logger.info("Connections closed")
