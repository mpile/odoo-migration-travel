# main.py
import logging
from config.settings import ODOO_CONFIG
from core.rpc_client import OdooRPCClient
from migrations.partners import PartnerMigrator
from migrations.products import ProductMigrator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("🚀 Starting Odoo Migration Tool...")
    
    odoo_client = None
    try:
        # Connect to Odoo and MySQL
        odoo_client = OdooRPCClient(ODOO_CONFIG)
        
        logger.info("📦 Running partner migration...")
        partner_migrator = PartnerMigrator(odoo_client)
        partner_migrator.migrate_partners()
        
        logger.info("📦 Running product migration...")
        product_migrator = ProductMigrator(odoo_client)
        product_migrator.migrate_products()
        
        logger.info("✅ All migrations completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Migration failed: {e}")
    finally:
        if odoo_client:
            odoo_client.close()

if __name__ == "__main__":
    main()
