# migrations/partners.py
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class PartnerMigrator:
    def __init__(self, odoo_client):
        self.odoo = odoo_client
    
    def cleanup_previous_partners(self):
        """Brisanje prethodno migriranih partnera"""
        logger.info("Cleaning up previous partners...")
        try:
            self.odoo.delete_records('res.partner', [('id', '>=', 100)])
            logger.info("✅ Previous partners cleaned up")
        except Exception as e:
            logger.error(f"❌ Cleanup failed: {e}")
    
    def migrate_partners(self):
        """Migracija partnera iz MySQL u Odoo"""
        logger.info("Starting partner migration...")
        
        try:
            self.cleanup_previous_partners()
            
            # Uzmi podatke iz MySQL
            self.odoo.mysql_cursor.execute("""
                SELECT SifraPoslovnogPartnera, NazivPoslovnogPartnera,
                       AdresaPoslovnogPartnera, MestoPoslovnogPartnera, PostaPoslovnogPartnera,
                       PIB, MaticniPoslovnogPartnera,
                       EmailPoslovnogPartnera, TelefonPoslovnogPartnera
                FROM poslovnipartneri
            """)
            rows = self.odoo.mysql_cursor.fetchall()
            
            logger.info(f"Found {len(rows)} partners to migrate")
            
            for row in rows:
                try:
                    partner_data = {
                        'id': row[0] + 100,  # Zadržavamo originalni ID + 100
                        'name': row[1] or 'Partner bez naziva',
                        'street': row[2] or False,
                        'city': row[3] or False,
                        'zip': row[4] or False,
                        'vat': row[5] or False,
                        'company_registry': row[6] or False,
                        'email': row[7] or False,
                        'phone': row[8] or False,
                        'is_company': True,
                        'active': True,
                        'country_id': 189,  # Srbija
                    }
                    
                    # Proveri da li postoji
                    existing = self.odoo.search_record('res.partner', [('id', '=', partner_data['id'])])
                    
                    if existing:
                        self.odoo.update_record('res.partner', existing[0], partner_data)
                        logger.info(f"✅ Updated partner ID {partner_data['id']}")
                    else:
                        self.odoo.create_record('res.partner', partner_data)
                        logger.info(f"✅ Created partner ID {partner_data['id']}")
                        
                except Exception as e:
                    logger.error(f"❌ Error with partner ID {row[0]}: {e}")
                    continue
            
            logger.info("✅ Partner migration completed successfully!")
            
        except Exception as e:
            logger.error(f"❌ Partner migration failed: {e}")
            raise
