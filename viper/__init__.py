from werkzeug.wrappers import Request

from viper.cores.core_log import logger
from viper.cores.core_http import abort

url_map = {}
url_map.update(todo_route)


def error_404(request):
    return abort(404)


def dispatch_request(request):
    path = request.path
    view_func = url_map.get(path, error_404)
    try:
        response = view_func(request)
    except (Exception,):
        logger.exception('Internal Server Error')
        return abort(500)
    return response


def wsgi_app(environ, start_response):
    request = Request(environ)
    response = dispatch_request(request)
    return response(environ, start_response)
