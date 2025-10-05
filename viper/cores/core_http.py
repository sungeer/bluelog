import orjson

from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.wrappers import Response as BaseResponse


class Response(BaseResponse):

    def __init__(self, response, **kwargs):
        payload = orjson.dumps(response)  # bytes
        kwargs.pop('mimetype', None)
        super().__init__(payload, content_type='application/json', **kwargs)


class ResponseModel:

    def __init__(self):
        self.status = True
        self.error_code = None
        self.error_message = None
        self.data = None

    def to_dict(self):
        resp_dict = {
            'status': self.status,
            'error_code': self.error_code,
            'error_message': self.error_message,
            'data': self.data
        }
        return resp_dict


def jsonify(*args, **kwargs):
    if args and kwargs:
        raise TypeError('jsonify() behavior undefined when passed both args and kwargs')
    elif len(args) == 1:
        content = args[0]
    else:
        content = kwargs or list(args)  # {}
    response = ResponseModel()
    response.data = content
    response = response.to_dict()
    return Response(response)


def abort(error_code, error_message=None):
    if not error_message:
        error_message = HTTP_STATUS_CODES.get(error_code)
    response = ResponseModel()
    response.status = False
    response.error_code = error_code
    response.error_message = error_message
    response = response.to_dict()
    return Response(response)
