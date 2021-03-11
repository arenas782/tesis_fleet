import os
from flask import Blueprint,render_template,redirect,url_for,request,flash
from flask import current_app as app
from .. import login_manager
from werkzeug.utils import secure_filename
from ..models import Driver,db,Vehicle
from sqlalchemy import or_
import uuid

from ..utils import role_required   
from flask_login import login_required, logout_user, current_user, login_user, logout_user

# Blueprint Configuration
drivers_bp = Blueprint(
    'drivers_bp', __name__,url_prefix='/drivers')


@drivers_bp.before_request
@login_required
def before_request():
    for user_role in current_user.roles:
        if (user_role.name=='admin' or user_role.name=='personal'):
            pass
        else:
            flash('No está autorizado para acceder a esta sección')
            return redirect(url_for('home_bp.dashboard'))    
    pass 


@drivers_bp.route('/')
def home():
    drivers = Driver.query.all()
    return render_template(
        'drivers/index.html',        
        segment = 'drivers',
        drivers = drivers,
        current_user=current_user,        
    )

@drivers_bp.route('/<id>')
def profile(id):
    driver = Driver.query.get(id)
    return render_template(
        'drivers/profile.html',        
        segment = 'drivers',
        driver = driver,
        current_user=current_user,        
    )


@drivers_bp.route('add',methods=['GET','POST'])
def add():
    if (request.method=='POST'):
            newDriver = Driver(dni=request.values.get('dni'),
                            name=request.values.get('name'),
                            lastname=request.values.get('lastname'),
                            address=request.values.get('address'),
                            phone=request.values.get('phone'),
                            email=request.values.get('email'))
            
            file = request.files['photo']
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER']+'/drivers', filename))
                newDriver.photo = filename            
            if(request.values.get('vehicle_id')):            
                vehicle = Vehicle.query.get(request.values.get('vehicle_id'))
                newDriver.vehicles.append(vehicle)

            
            newDriver.create()
            flash('Nuevo conductor registrado','success')
            return redirect(url_for('drivers_bp.home'))    
            #except:
            #flash('Ha ocurrido un error','danger')
            #return redirect(url_for('drivers_bp.home'))    
    else:                
        vehicles = Vehicle.query.filter_by(driver_id=None).all()
        return render_template(
            'drivers/add-form.html',            
            segment = 'drivers',    
            vehicles = vehicles,
            current_user = current_user
        )   

@drivers_bp.route('/edit/<id>',methods=['GET','POST'])
def edit(id):
    if request.method=='POST' :               
        driver= Driver.query.get(request.values.get('driver_id'))
        driver.name=request.values.get('name')
        driver.lastname=request.values.get('lastname')
        driver.phone=request.values.get('phone') or None
        driver.email=request.values.get('email') or None
        driver.address=request.values.get('address') or None   
        driver.vehicles=[]
        if(request.values.get('vehicle_id')):            
            vehicle = Vehicle.query.get(request.values.get('vehicle_id'))
            vehicle.driver=driver     
        
        driver.update()
        flash('Datos modificados','success')
        return redirect(url_for('drivers_bp.home'))    
    else:
        driver = Driver.query.get(id)
        vehicles = Vehicle.query.filter(or_(Vehicle.driver_id==None, Vehicle.driver_id==id)).all()            
        return render_template(
            'drivers/edit-form.html',            
            segment = 'drivers',    
            driver = driver,
            vehicles = vehicles,
            current_user = current_user
        )   
