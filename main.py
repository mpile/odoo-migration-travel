# main.py
import logging
from config.settings import ODOO_CONFIG, MYSQL_CONFIG
from core.rpc_client import OdooRPCClient
from migrations.partners import PartnerMigrator
from migrations.products import ProductMigrator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("🚀 Starting Odoo Migration...")
    
    try:
        # Connect to Odoo
        odoo_client = OdooRPCClient(ODOO_CONFIG)
        
        # Run migrations
        partner_migrator = PartnerMigrator(odoo_client, None)
        partner_migrator.migrate_partners()
        
        product_migrator = ProductMigrator(odoo_client, None)
        product_migrator.migrate_products()
        
        logger.info("✅ All migrations completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Migration failed: {e}")

if __name__ == "__main__":
    main()
