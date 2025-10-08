from functools import wraps

from viper.cores.core_http import abort


# 强制POST请求
def require_post(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.method != 'POST':
            return abort(405)
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def require_get(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.method != 'GET':
            return abort(405)
        return view_func(request, *args, **kwargs)

    return _wrapped_view
