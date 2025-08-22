import logging
from pathlib import Path

from viper.core import settings

log_dir = Path(settings.BASE_DIR) / 'logs'
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / 'huey.log'

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setFormatter(formatter)

logger = logging.getLogger('huey')

logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
