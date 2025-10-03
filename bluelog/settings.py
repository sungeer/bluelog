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

    DATABASE_USERNAME = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_USERNAME')
    DATABASE_PASSWORD = os.getenv('MAIL_USERNAME')

    SHORTLY_PER_PAGE = 10
    SHORTLY_MANAGE_PER_PAGE = 15
    SHORTLY_THEMES = {'default': 'Default', 'shortly': 'Shortly'}

    SHORTLY_UPLOAD_PATH = os.getenv('SHORTLY_UPLOAD_PATH', BASE_DIR / 'uploads')
    SHORTLY_ALLOWED_IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif']
    SHORTLY_LOGGING_PATH = os.getenv('SHORTLY_LOGGING_PATH', BASE_DIR / 'logs/shortly.log')
    SHORTLY_ERROR_EMAIL_SUBJECT = '[Shortly] Application Error'


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
