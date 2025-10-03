from flask import Flask

from bluelog.blueprints.auth import auth_bp
from bluelog.blueprints.blog import blog_bp
from bluelog.core.errors import register_errors
from bluelog.core.logging import register_logging
from bluelog.settings import config


def create_app(config_name):
    app = Flask('bluelog')
    app.config.from_object(config[config_name])

    # blueprints
    app.register_blueprint(blog_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # extensions
    pass

    register_logging(app)
    register_errors(app)

    return app