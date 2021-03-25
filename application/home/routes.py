from flask import Blueprint,render_template,redirect,url_for,flash
from flask import current_app as app
from ..models import db, User
from .. import login_manager
from ..utils import role_required   
from ..models import Driver,Vehicle,Tracker,User
from flask_login import login_required, logout_user, current_user
# Blueprint Configuration
home_bp = Blueprint(
    'home_bp', __name__,url_prefix='/')


@home_bp.before_request
@login_required
def before_request():    
    if (current_user.role.name=='admin' or current_user.role.name=='personal' or current_user.role.name=='taller' or current_user.role.name=='operador'  ):
        pass
    else:
        flash('No está autorizado para acceder a esta sección','error')
        return redirect(url_for('home_bp.dashboard'))    
    


@home_bp.route('/')
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
def reports():
    return render_template(
        'reports.html',
        current_user=current_user
    )




