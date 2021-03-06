from flask import Blueprint,render_template,redirect,url_for,request,flash
from flask import current_app as app
from werkzeug.utils import secure_filename
import os

from .. import login_manager
from ..models import Vehicle,VehicleBrand,Driver,VehicleType,VehicleStatus,Fleet
from ..utils import role_required   
from ..models import db
from flask_login import login_required, logout_user, current_user, login_user, logout_user

# Blueprint Configuration
vehicles_bp = Blueprint(
    'vehicles_bp', __name__,url_prefix='/vehicles')

@vehicles_bp.before_request
@login_required
def before_request():    
    if (current_user.role.name=='admin' or current_user.role.name=='operador'):
        pass
    else:
        flash('No está autorizado para acceder a esta sección','error')
        return redirect(url_for('home_bp.dashboard'))    


@vehicles_bp.route('/')
def home():
    rows_per_page = 15
    page = request.args.get('page', 1, type=int)
    query = request.args.get('query')
    status_id = request.args.get('status_id')
    fleet_id = request.args.get('fleet_id')
    vehicles = Vehicle.query
    if query:        
        vehicles = vehicles.filter(Vehicle.plate.like('%'+query+'%'))
    if status_id:
        vehicles = vehicles.filter(Vehicle.vehicle_status_id==status_id)
    if fleet_id:
        vehicles = vehicles.filter(Vehicle.fleet_id==fleet_id)
    

    vehicles = vehicles.order_by(Vehicle.created_at.desc()).paginate(page=page,per_page=rows_per_page)
    vehicles_status = VehicleStatus.query.all()
    fleets = Fleet.query.all()
                        
    return render_template(
        'vehicles/index.html',        
        segment = 'vehicles',
        query = query,
        status_id = status_id,
        fleet_id = fleet_id,
        fleets = fleets,
        vehicles_status = vehicles_status,
        vehicles = vehicles,
        current_user=current_user,        
    )

@vehicles_bp.route('/<id>')
def detail(id):
    vehicle = Vehicle.query.get(id)
    return render_template(
        'vehicles/detail.html',        
        segment = 'vehicles',
        vehicle = vehicle,
        current_user=current_user,        
    )

@vehicles_bp.route('/add', methods=["GET", "POST"])
def add():
    if (request.method=='POST'):
            ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


            newVehicle = Vehicle(plate=request.values.get('plate'),
                            color=request.values.get('color'),
                            brand_id=request.values.get('brand_id'),
                            driver_id=request.values.get('driver_id') or None,
                            fleet_id = request.values.get('fleet_id') or None,
                            vehicle_status_id=request.values.get('vehicle_status_id'),
                            model=request.values.get('model'),
                            vehicle_type_id=request.values.get('vehicle_type_id'),
                            year=request.values.get('year'))
            file = request.files['photo']
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER']+'/vehicles', filename))
                newVehicle.photo = filename
            
            try:
                db.session.add(newVehicle)
                db.session.commit()
                flash('Nuevo vehículo registrado','success')                
            except:
                flash('Ha ocurrido un error','danger')
            return redirect(url_for('vehicles_bp.home'))    
    else:
        #select only drivers witouth assigned vehicle
        drivers = db.engine.execute("select * from drivers where id not in (select driver_id from vehicles where driver_id is not null)")
        brands = VehicleBrand.query.all()
        vehicles_types = VehicleType.query.all()
        fleets = Fleet.query.all()
        vehicles_status = VehicleStatus.query.all()

        
        return render_template(
            'vehicles/add-form.html',
            brands = brands,
            fleets = fleets,
            drivers = drivers,
            vehicles_status = vehicles_status,
            segment = 'vehicles',    
            vehicles_types = vehicles_types,
            current_user = current_user
        )   

@vehicles_bp.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    vehicle = Vehicle.query.get(id)
    brands = VehicleBrand.query.all()
    
    if(request.method=="POST"):
        vehicle= Vehicle.query.get(request.values.get('vehicle_id'))
        vehicle.color=request.values.get('color')
        vehicle.model=request.values.get('model')
        vehicle.brand_id=request.values.get('brand_id')
        vehicle.driver_id=request.values.get('driver_id') or None
        vehicle.year=request.values.get('year')
        vehicle.vehicle_type_id = request.values.get('vehicle_type_id'),
        vehicle.vehicle_status_id = request.values.get('vehicle_status_id'),
        vehicle.fleet_id = request.values.get('fleet_id') or None

        db.session.commit()
        flash('Datos modificados','success')
        return redirect(url_for('vehicles_bp.home'))    
    else:
        if(vehicle.driver_id is not None):
            drivers = db.engine.execute("select * from drivers where id not in (select driver_id from vehicles where driver_id is not null and driver_id!={})".format(vehicle.driver_id))
        else:
            drivers = db.engine.execute("select * from drivers where id not in (select driver_id from vehicles where driver_id is not null )")
        
        vehicles_types = VehicleType.query.all()
        vehicles_status = VehicleStatus.query.all()
        fleets = Fleet.query.all()

        return render_template(
            'vehicles/edit-form.html',
            brands = brands,
            fleets = fleets,
            drivers = drivers,
            segment = 'vehicles',    
            vehicles_status = vehicles_status,
            vehicles_types = vehicles_types,
            vehicle = vehicle,
            current_user = current_user
        )   

@vehicles_bp.route('/delete/<id>')
def delete(id):    
    vehicle = Vehicle.query.get(id)
    if vehicle:
        vehicle.delete()
        flash('Vehículo eliminado','success')
    else:
        flash('Vehículo no encontrado','error')
    return redirect(url_for('vehicles_bp.home'))    