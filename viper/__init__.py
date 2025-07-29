from werkzeug.wrappers import Request

from viper.core.routes import response_for_path


def app(environ, start_response):
    request = Request(environ)
    response = response_for_path(request)
    return response(environ, start_response)
