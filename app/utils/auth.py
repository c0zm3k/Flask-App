from functools import wraps
from flask import session, redirect, url_for, flash, request

def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user = session.get('user')
            if not user:
                flash('Please log in first.', 'warning')
                return redirect(url_for('auth.login_select'))
            if role and user.get('role') != role:
                flash('Unauthorized.', 'danger')
                return redirect(url_for('auth.login_select'))
            return f(*args, **kwargs)
        return wrapper
    return decorator

def set_user(role, user_id, username):
    session['user'] = {'role': role, 'id': user_id, 'username': username}

def clear_user():
    session.pop('user', None)
