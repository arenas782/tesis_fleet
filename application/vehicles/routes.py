from flask import Blueprint,render_template,redirect,url_for,request,flash
from flask import current_app as app
from werkzeug.utils import secure_filename
import os

from .. import login_manager
from ..models import Vehicle,VehicleBrand,Driver
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
    rows_per_page = 3
    page = request.args.get('page', 1, type=int)
    query = request.args.get('query')
    if query:        
        vehicles = Vehicle.query.filter(Vehicle.plate.like('%'+query+'%')).order_by(Vehicle.created_at.desc()).paginate(page=page,per_page=rows_per_page)                   
    else:        
        vehicles = Vehicle.query.order_by(Vehicle.created_at.desc()).paginate(page=page,per_page=rows_per_page)                           
    return render_template(
        'vehicles/index.html',        
        segment = 'vehicles',
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
            ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


            newVehicle = Vehicle(plate=request.values.get('plate'),
                            color=request.values.get('color'),
                            brand_id=request.values.get('brand_id'),
                            driver_id=request.values.get('driver_id') or None,
                            model=request.values.get('model'),
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
                return redirect(url_for('vehicles_bp.home'))    
            except:
                flash('Ha ocurrido un error','danger')
                return redirect(url_for('vehicles_bp.home'))    
    else:
        #select only drivers witouth assigned vehicle
        drivers = db.engine.execute("select * from drivers where id not in (select driver_id from vehicles where driver_id is not null)")
        brands = VehicleBrand.query.all()
        
        return render_template(
            'vehicles/add-form.html',
            brands = brands,
            drivers = drivers,
            segment = 'vehicles',    
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
        db.session.commit()
        flash('Datos modificados','success')
        return redirect(url_for('vehicles_bp.home'))    
    else:
        if(vehicle.driver_id is not None):
            drivers = db.engine.execute("select * from drivers where id not in (select driver_id from vehicles where driver_id is not null and driver_id!={})".format(vehicle.driver_id))
        else:
            drivers = db.engine.execute("select * from drivers where id not in (select driver_id from vehicles where driver_id is not null )")
        
        return render_template(
            'vehicles/edit-form.html',
            brands = brands,
            drivers = drivers,
            segment = 'vehicles',    
            vehicle = vehicle,
            current_user = current_user
        )   

