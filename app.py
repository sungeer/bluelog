from viper import wsgi_app

from werkzeug.serving import run_simple


run_simple('127.0.0.1', 5000, wsgi_app, threaded=True)
