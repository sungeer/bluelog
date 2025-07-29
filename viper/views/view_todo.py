from viper.wrappers.response import jsonify

from viper.utils import util_pool
from viper.services import service_todo


def get_todos(request):
    x = int(request.args.get('x', 1))
    future = util_pool.pool_thread_common.submit(service_todo.func_a, x)
    result = future.result(timeout=3)
    return jsonify(result)


route_dict = {
    '/api/get_todos': get_todos,
}
