from flask import Blueprint,render_template,redirect,url_for,flash
from flask import current_app as app
from ..models import db, User
from .. import login_manager
from ..utils import role_required   
from ..models import Driver,Vehicle,Tracker,User,Maintenance,VehicleType,Vehicle,VehicleStatus
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
    maintenances_pending = Maintenance.query.filter_by(status="Pendiente").count()
    maintenances_inprocess = Maintenance.query.filter_by(status="En proceso").count()
    maintenances_completed = Maintenance.query.filter_by(status="Completado").count()
    maintenances_stats = [maintenances_pending,maintenances_inprocess,maintenances_completed]
    total_drivers = Driver.query.count()
    total_vehicles = Vehicle.query.count()
    total_trackers = Tracker.query.count()

    vehicleTypes = VehicleType.query.all()
    vehicles_per_type=[]
    for vehicleType in vehicleTypes:
        vehiclesOfType = Vehicle.query.filter(Vehicle.vehicle_type_id==vehicleType.id).count()
        vehicles_per_type.append([vehicleType.description,vehiclesOfType])


    vehicleStatuses = VehicleStatus.query.all()
    vehicles_per_status=[]
    for vehicleStatus in vehicleStatuses:
        vehiclesOfStatus = Vehicle.query.filter(Vehicle.vehicle_status_id==vehicleStatus.id).count()
        vehicles_per_status.append([vehicleStatus.name,vehiclesOfStatus])

    total_users = User.query.count()
    return render_template(
        'index.html',        
        segment = 'dashboard',
        maintenances_stats = maintenances_stats,
        vehicles_per_type = vehicles_per_type,
        vehicles_per_status = vehicles_per_status,
        total_drivers = total_drivers,
        total_vehicles = total_vehicles,
        total_trackers = total_trackers,        
        total_users = total_users,
        current_user=current_user,        
    )




