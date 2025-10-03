from functools import wraps

from flask import g, url_for, redirect


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)

    return decorated_function
