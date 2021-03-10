from flask import Blueprint,render_template,redirect,url_for
from flask import current_app as app
from ..models import db, User
from .. import login_manager
from ..utils import role_required   
from ..models import Driver,Vehicle,Tracker,User
from flask_login import login_required, logout_user, current_user, login_user, logout_user
# Blueprint Configuration
home_bp = Blueprint(
    'home_bp', __name__,url_prefix='/')

@home_bp.route('/')
@login_required

def dashboard():
    total_drivers = Driver.query.count()
    total_vehicles = Vehicle.query.count()
    total_trackers = Tracker.query.count()
    total_users = User.query.count()
    return render_template(
        'index.html',        
        segment = 'dashboard',
        total_drivers = total_drivers,
        total_vehicles = total_vehicles,
        total_trackers = total_trackers,
        total_users = total_users,
        current_user=current_user,        
    )

@home_bp.route('/reports')
@login_required
@role_required('admin')
def reports():
    return render_template(
        'reports.html',
        current_user=current_user
    )


@home_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))

    

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None

