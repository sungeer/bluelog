from viper.wrappers.response import jsonify


def get_todos(request):
    data = {'abc': 'qaz'}
    return jsonify(data)


route_dict = {
    '/api/get_todos': get_todos,
}
