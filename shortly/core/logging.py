import logging
from logging.handlers import RotatingFileHandler


def register_logging(app):
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
    logging_path = app.config['LOGGING_PATH']
    file_handler = RotatingFileHandler(logging_path, maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    if not app.debug:
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
