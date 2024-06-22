from functools import wraps
from flask import abort, redirect, url_for
from flask_login import current_user


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('main.login'))
        if current_user.role != 'admin':
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)

    return decorated_function


def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('main.login'))
        if current_user.role != 'user':
            abort(403)  # Forbidden
        return f(*args, **kwargs)

    return decorated_function
