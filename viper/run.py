from gevent import monkey

monkey.patch_all(thread=False, subprocess=False)

import signal
from datetime import datetime

from werkzeug.wrappers import Request
from gevent.pywsgi import WSGIServer

from viper.core.routes import response_for_path


def application(environ, start_response):
    request = Request(environ)
    response = response_for_path(request)
    return response(environ, start_response)


def stop_server(signum, frame):
    print('\nShutting down')
    server.stop()
    print('Finished server process')


print(f'* Running on http://{'127.0.0.1'}:7788 (Press CTRL+C to quit)')
print(f'* Using worker: gevent.pywsgi.WSGIServer')
print(f'* Started at {datetime.now().isoformat(sep=' ', timespec='seconds')}')
server = WSGIServer(('0.0.0.0', 7788), application)
signal.signal(signal.SIGINT, stop_server)
server.serve_forever()
