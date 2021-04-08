from flask import Blueprint,render_template,redirect,url_for,request,flash
from flask import current_app as app
from .. import login_manager
from ..models import Fleet,FleetType,Vehicle

from sqlalchemy import and_,or_
from flask_login import login_required, logout_user, current_user, login_user, logout_user
from datetime import date
import sys



# Blueprint Configuration
fleets_bp = Blueprint(
    'fleets_bp', __name__,url_prefix='/fleets')

@fleets_bp.before_request
@login_required
def before_request():    
    if (current_user.role.name=='admin'):
        pass
    else:
        flash('No está autorizado para acceder a esta sección','error')
        return redirect(url_for('home_bp.dashboard'))    
         

@fleets_bp.route('/')
def home():            
    fleets = Fleet.query.order_by(Fleet.created_at.desc()).all()
    
    vehicles_per_fleet=[]
    for fleet in fleets:
        vehiclesOfFleet= Vehicle.query.filter(Vehicle.fleet_id==fleet.id).count()
        vehicles_per_fleet.append([fleet.id,fleet.name,fleet.fleet_type.name,fleet.created_at,vehiclesOfFleet])

    return render_template(
        'fleets/index.html',        
        segment = 'fleets',        
        fleets = vehicles_per_fleet,        
        
        current_user=current_user,        
    )

@fleets_bp.route('/add',methods=['GET','POST'])
def add():
    if request.method=='POST':
        newFleet = Fleet(name=request.values.get('name'),fleet_type_id=request.values.get('fleet_type_id'))
        try:
            newFleet.create()
            flash('Nueva flota registrado','success')
            return redirect(url_for('fleets_bp.home'))    
        except:
            flash('Ha ocurrido un error','danger')
            return redirect(url_for('fleets_bp.home'))                                
    else:
        fleet_types = FleetType.query.all()        
        return render_template(
            'fleets/add-form.html',        
            segment = 'fleets',            
            fleet_types = fleet_types,            
            current_user=current_user,        
        )
@fleets_bp.route('/<id>')
def detail(id):
    fleet = Fleet.query.get(id)
    vehicles = Vehicle.query.filter(Vehicle.fleet_id==fleet.id).all()
    return render_template(
        'fleets/detail.html',        
        segment = 'fleets',
        fleet = fleet,
        vehicles = vehicles,
        current_user=current_user,        
    )
@fleets_bp.route('/edit/<id>',methods=['GET','POST'])
def edit(id):
    if request.method=='POST':
        fleet =Fleet.query.get(request.values.get('fleet_id'))
        fleet.name = request.values.get('name')
        fleet.fleet_type_id = request.values.get('fleet_type_id') 
        
        try:
            fleet.update()
            flash('Datos modificados','success')
            return redirect(url_for('fleets_bp.home'))    
        except:
            flash('Ha ocurrido un error','danger')
            return redirect(url_for('fleets_bp.home'))                                
    else:
        fleet_types = FleetType.query.all()
        fleet = Fleet.query.get(id)
        
        if fleet:        
            return render_template(
                'fleets/edit-form.html',        
                segment = 'fleets',
                fleet = fleet,             
                fleet_types = fleet_types,   
                current_user=current_user,                
            )
        else:
            flash('Flota no encontrada','danger')
            return render_template(
                'fleets/index.html',        
                segment = 'fleets',                
                current_user=current_user,                
            )



@fleets_bp.route('/delete/<id>')
def delete(id):    
    fleet = Fleet.query.get(id)
    if fleet:
        fleet.delete()
        flash('Flota eliminada','success')
    else:
        flash('Flota no encontrada','error')
    return redirect(url_for('fleets_bp.home'))    

@fleets_bp.route('/print_vehicles/<id>')
def print_vehicles(id):
    from flask_weasyprint import HTML, render_pdf    
    
    
    fleet = Fleet.query.get(id)

    if fleet:
        fleet_vehicles = Vehicle.query.filter_by(fleet_id=fleet.id).order_by(Vehicle.created_at.desc()).all()        
        html = render_template('fleets/pdf_fleet_vehicles.html', fleet=fleet,fleet_vehicles=fleet_vehicles)
        pdfname=fleet.name+'.pdf'
        return render_pdf(HTML(string=html))
        #return render_template('trackers/pdf_logs.html', logs=logs,tracker=tracker,from_date=from_date,to_date=to_date)
    else:
        return 'error'

