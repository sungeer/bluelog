import os
from datetime import datetime
from pathlib import Path

with_debug = os.getenv('DEBUG') == '1'

base_dir = Path(__file__).resolve().parent.parent

# db
database_username = os.getenv('DATABASE_USERNAME')
database_password = os.getenv('DATABASE_PASSWORD')
database_host = os.getenv('DATABASE_HOST')
database_port = int(os.getenv('DATABASE_PORT'))
database_name = os.getenv('DATABASE_NAME')

# log
log_dir = base_dir / 'logs'
log_path = log_dir / f'{datetime.now().strftime('%Y-%m-%d')}.log'
