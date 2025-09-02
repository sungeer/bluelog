from http import HTTPStatus

from starlette.responses import JSONResponse
from starlette.responses import StreamingResponse

from viper.utils import util_json


class JsonExtendResponse(JSONResponse):

    def render(self, content):
        return util_json.dict_to_json_stream(content)


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
        content = args or kwargs
    response = BaseResponse()
    response.data = content
    response = response.to_dict()
    return JsonExtendResponse(response)


def abort(error_code, message=None):
    if not message:
        message = HTTPStatus(error_code).phrase
    response = BaseResponse()
    response.status = False
    response.error_code = error_code
    response.message = message
    response = response.to_dict()
    return JsonExtendResponse(response)


def sseify(event_generator):
    async def wrapper():
        async for data in event_generator():
            # return f'data: {json.dumps(data)}\n\n'
            payload = BaseResponse()
            payload.data = data
            payload = payload.to_dict()
            sse_data = f'data: {util_json.dict_to_json(payload)}\n\n'
            yield sse_data
    return StreamingResponse(wrapper(), media_type='text/event-stream')
