# migrations/products.py
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ProductMigrator:
    def __init__(self, odoo_client):
        self.odoo = odoo_client
    
    def cleanup_previous_products(self):
        """Brisanje prethodno migriranih proizvoda"""
        logger.info("Cleaning up previous products...")
        try:
            self.odoo.delete_records('product.template', [('id', '>=', 1)])
            logger.info("✅ Previous products cleaned up")
        except Exception as e:
            logger.error(f"❌ Product cleanup failed: {e}")
    
    def get_tax_ids(self, stopa_pdv):
        """Mapiranje PDV stope na Odoo porezne ID-ijeve"""
        try:
            # Prilagodi ove ID-ijeve prema tvom Odoo sistemu
            tax_mapping = {
                20: 1,  # PDV 20%
                10: 2,  # PDV 10% 
                0: 3,   # PDV 0%
            }
            
            stopa = int(float(stopa_pdv or 0))
            tax_id = tax_mapping.get(stopa, 1)  # Default 20%
            return [tax_id]
            
        except Exception as e:
            logger.warning(f"Tax mapping error for {stopa_pdv}, using default: {e}")
            return [1]
    
    def migrate_products(self):
        """Migracija proizvoda iz MySQL u Odoo"""
        logger.info("Starting product migration...")
        
        try:
            self.cleanup_previous_products()
            
            # Uzmi podatke iz MySQL
            self.odoo.mysql_cursor.execute("""
                SELECT SifraProizvoda, NazivProizvoda, StopaPDV, Code, VpCena 
                FROM proizvodi
            """)
            rows = self.odoo.mysql_cursor.fetchall()
            
            logger.info(f"Found {len(rows)} products to migrate")
            
            for row in rows:
                try:
                    product_data = {
                        'id': row[0],  # Zadržavamo originalni ID
                        'name': row[1] or 'Proizvod bez naziva',
                        'default_code': row[3] or f"PROD{row[0]}",
                        'list_price': float(row[4] or 0),
                        'type': 'service',
                        'categ_id': 1,  # Default kategorija
                        'purchase_ok': False,
                        'sale_ok': True,
                        'active': True,
                        'taxes_id': [(6, 0, self.get_tax_ids(row[2]))],
                        'supplier_taxes_id': [(6, 0, [])],
                    }
                    
                    # Proveri da li postoji
                    existing = self.odoo.search_record('product.template', [('id', '=', product_data['id'])])
                    
                    if existing:
                        self.odoo.update_record('product.template', existing[0], product_data)
                        logger.info(f"✅ Updated product ID {product_data['id']}")
                    else:
                        self.odoo.create_record('product.template', product_data)
                        logger.info(f"✅ Created product ID {product_data['id']}")
                        
                except Exception as e:
                    logger.error(f"❌ Error with product ID {row[0]}: {e}")
                    continue
            
            # Loguj ukupan broj
            self.odoo.mysql_cursor.execute("SELECT COUNT(SifraProizvoda) FROM proizvodi")
            count = self.odoo.mysql_cursor.fetchone()[0]
            logger.info(f"✅ Product migration completed! Total: {count} products")
            
        except Exception as e:
            logger.error(f"❌ Product migration failed: {e}")
            raise
