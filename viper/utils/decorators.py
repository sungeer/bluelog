from functools import wraps

from viper.schemas import validator
from viper.utils.resp_util import abort
from viper.utils.pools import run_in_thread_pool_db


def validate_request(schema):
    def decorator(func):
        @wraps(func)
        async def decorated_function(request, *args, **kwargs):
            data = await request.json()
            validator(data, schema)
            return await func(request, *args, **kwargs)

        return decorated_function

    return decorator


def permission_required(permission_name):
    def decorator(func):
        @wraps(func)
        async def decorated_function(request, *args, **kwargs):
            perm = request.state.has_perm
            if perm not in (permission_name,):
                return abort(403)
            return await func(request, *args, **kwargs)

        return decorated_function

    return decorator


def admin_required(func):  # @admin_required
    return permission_required('admin')(func)


def sync_to_async_db(func):
    @wraps(func)
    async def async_run_in_thread_pool(*args, **kwargs):
        return await run_in_thread_pool_db(func, *args, **kwargs)

    return async_run_in_thread_pool
