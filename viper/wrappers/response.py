import json

from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.wrappers import Response as ResponseBase

from viper.utils import util_json


class Response(ResponseBase):

    default_mimetype: str | None = 'text/html'

    json_module = json

    autocorrect_location_header = False


class JsonExtendResponse(Response):

    def __init__(self, response, **kwargs):
        json_response = util_json.dict_to_json_stream(response)
        super().__init__(json_response, mimetype='application/json', **kwargs)


class BaseResponse:

    def __init__(self):
        self.status = True
        self.error_code = None
        self.message = None
        self.data = None

    def to_dict(self):
        resp_dict = {
            'status': self.status,
            'error_code': self.error_code,
            'message': self.message,
            'data': self.data
        }
        return resp_dict


def jsonify(*args, **kwargs):
    if args and kwargs:
        raise TypeError('jsonify() behavior undefined when passed both args and kwargs')
    elif len(args) == 1:
        content = args[0]
    else:
        content = args or kwargs  # {}
    response = BaseResponse()
    response.data = content
    response = response.to_dict()
    return JsonExtendResponse(response)


def abort(error_code, message=None):
    if not message:
        message = HTTP_STATUS_CODES.get(error_code)
    response = BaseResponse()
    response.status = False
    response.error_code = error_code
    response.message = message
    response = response.to_dict()
    return JsonExtendResponse(response)
