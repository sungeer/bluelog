import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')

    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DEBUG_TB_ENABLED = False

    SQLALCHEMY_RECORD_QUERIES = True

    CKEDITOR_ENABLE_CSRF = True
    CKEDITOR_FILE_UPLOADER = 'admin.upload_image'

    DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
    DATABASE_PORT = os.getenv('DATABASE_PORT')

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
