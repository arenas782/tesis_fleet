from functools import wraps
from flask_login import current_user
from flask import url_for,redirect,flash


def role_required(role):
    def inner_decorator(f):
        def wrapped(*args, **kwargs):
            for user_role in current_user.roles:
                if (user_role.name==role):
                    return f(*args, **kwargs)
                else:
                    flash('No está autorizado para acceder a esta sección')
                    return redirect(url_for('home_bp.dashboard'))    
        return wrapped
    return inner_decorator
