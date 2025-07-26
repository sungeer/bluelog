from gevent import monkey

monkey.patch_all(thread=False, subprocess=False)

import sys
import signal

from gevent.pywsgi import WSGIServer

from viper.utils.util_log import logger


def handle_uncaught_exception(exc_type, exc_value, exc_traceback):
    logger.opt(exception=(exc_type, exc_value, exc_traceback)).critical('Critical exception, application will shutdown.')


sys.excepthook = handle_uncaught_exception


def application(environ, start_response):
    try:
        method = environ['REQUEST_METHOD']
        raise
        path = environ['PATH_INFO']
        query = environ['QUERY_STRING']
        headers = {k[5:]: v for k, v in environ.items() if k.startswith('HTTP_')}
        try:
            length = int(environ.get('CONTENT_LENGTH', 0) or 0)
        except (ValueError, TypeError):
            length = 0
        body = environ['wsgi.input'].read(length) if length > 0 else b''

        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [b'Hello, world!\n']
    except (Exception,):
        logger.exception('error from verifying')
        start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
        return [b'Internal Server Error\n']


def stop_server(signum, frame):
    print('\nReceived signal to stop server.')
    server.stop()


server = WSGIServer(('0.0.0.0', 8000), application)
signal.signal(signal.SIGINT, stop_server)
server.serve_forever()
