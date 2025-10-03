import os
from pathlib import Path

from dotenv import load_dotenv

dotenv_path = Path(__file__).resolve().parent / '.env'
if dotenv_path.exists():
    load_dotenv(dotenv_path)

from shortly import create_app  # noqa

config_name = os.getenv('FLASK_CONFIG', 'development')
app = create_app(config_name)
