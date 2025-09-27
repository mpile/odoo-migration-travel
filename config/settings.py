# config/settings.py
import os

# Odoo configuration
ODOO_CONFIG = {
    'url': os.getenv('ODOO_URL', 'http://localhost:8069'),
    'db': os.getenv('ODOO_DB', 'anstravel'),
    'username': os.getenv('ODOO_USERNAME', ''),
    'password': os.getenv('ODOO_PASSWORD', '')
}

# MySQL configuration
MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'database': os.getenv('MYSQL_DB', 'artinfo_ansdata2025'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', '')
}
