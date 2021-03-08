from flask import Blueprint,render_template,redirect,url_for
from flask import current_app as app
from .. import login_manager
from ..utils import role_required   
from flask_login import login_required, logout_user, current_user, login_user, logout_user

# Blueprint Configuration
users_bp = Blueprint(
    'users_bp', __name__,url_prefix='/users')

@users_bp.route('/')
@login_required
def home():
    return render_template(
        'users/index.html',        
        segment = 'users',
        current_user=current_user,        
    )