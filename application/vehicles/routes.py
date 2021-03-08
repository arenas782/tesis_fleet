from flask import Blueprint,render_template,redirect,url_for
from flask import current_app as app
from .. import login_manager
from ..utils import role_required   
from flask_login import login_required, logout_user, current_user, login_user, logout_user

# Blueprint Configuration
vehicles_bp = Blueprint(
    'vehicles_bp', __name__,url_prefix='/vehicles')

@vehicles_bp.route('/')
@login_required
def home():
    return render_template(
        'vehicles/index.html',        
        segment = 'vehicles',
        current_user=current_user,        
    )