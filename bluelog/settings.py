import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')

    DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
    DATABASE_HOST = os.getenv('DATABASE_HOST')
    DATABASE_PORT = os.getenv('DATABASE_PORT')
    DATABASE_NAME = os.getenv('DATABASE_NAME')

    BLUELOG_PER_PAGE = 10
    BLUELOG_MANAGE_PER_PAGE = 15
    BLUELOG_THEMES = {'default': 'Default', 'bluelog': 'Bluelog'}

    # BLUELOG_UPLOAD_PATH = os.getenv('BLUELOG_UPLOAD_PATH', BASE_DIR / 'uploads')
    BLUELOG_ALLOWED_IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif']
    BLUELOG_LOGGING_PATH = os.getenv('BLUELOG_LOGGING_PATH', BASE_DIR / 'logs/bluelog.log')
    BLUELOG_ERROR_EMAIL_SUBJECT = '[Bluelog] Application Error'


class DevelopmentConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    TESTING = True


class ProductionConfig(BaseConfig):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
