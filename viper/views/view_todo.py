from viper.wrappers.response import jsonify, sseify
from viper.services import service_todo


async def get_todos(request):
    data = {'abc': 'qaz'}
    return jsonify(data)


async def sse_todo():
    return sseify(service_todo.stream_data)


route_dict = {
    '/api/get_todos': get_todos,
}
