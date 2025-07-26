from gevent import monkey

monkey.patch_all(thread=False, subprocess=False)

import sys
import signal

from werkzeug.wrappers import Request
from gevent.pywsgi import WSGIServer

from viper.utils.util_log import logger
from viper.wrappers.response import jsonify


def handle_uncaught_exception(exc_type, exc_value, exc_traceback):
    logger.opt(exception=(exc_type, exc_value, exc_traceback)).critical('Critical exception, application will shutdown.')


sys.excepthook = handle_uncaught_exception


def application(environ, start_response):
    try:
        request = Request(environ)
        data = 'Hello, world!'
        response = jsonify(data)
        return response(environ, start_response)
    except (Exception,):
        logger.exception('error from verifying')
        start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
        return [b'Internal Server Error\n']


def stop_server(signum, frame):
    print('\nReceived signal to stop server.')
    server.stop()


server = WSGIServer(('0.0.0.0', 7788), application)
signal.signal(signal.SIGINT, stop_server)
server.serve_forever()
