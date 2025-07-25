from gevent import monkey

monkey.patch_all(thread=False, subprocess=False)

import signal

from gevent.pywsgi import WSGIServer


def application(environ, start_response):
    # 获取请求方法
    method = environ['REQUEST_METHOD']
    # 获取请求路径
    path = environ['PATH_INFO']
    # 获取请求查询字符串
    query = environ['QUERY_STRING']
    # 获取请求头
    headers = {k[5:]: v for k, v in environ.items() if k.startswith('HTTP_')}
    print(headers)
    # 获取请求体
    try:
        length = int(environ.get('CONTENT_LENGTH', 0) or 0)
    except (ValueError, TypeError):
        length = 0
    body = environ['wsgi.input'].read(length) if length > 0 else b''

    # 这里可以处理业务逻辑
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b'Hello, world!\n']


def stop_server(signum, frame):
    print('\nReceived signal to stop server.')
    server.stop()


server = WSGIServer(('0.0.0.0', 8000), application)
signal.signal(signal.SIGINT, stop_server)
server.serve_forever()
