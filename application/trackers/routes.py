from flask import Blueprint,render_template,redirect,url_for,request,flash
from flask import current_app as app
from .. import login_manager
from ..models import Tracker,Vehicle,db,TrackerProtocol,TrackerCommand,TrackerCommandHistory
from ..utils import role_required   
from sqlalchemy import and_,or_
from flask_login import login_required, logout_user, current_user, login_user, logout_user

# Blueprint Configuration
trackers_bp = Blueprint(
    'trackers_bp', __name__,url_prefix='/trackers')

@trackers_bp.before_request
@login_required
def before_request():
    for user_role in current_user.roles:
        if (user_role.name=='admin' or user_role.name=='operador'):
            pass
        else:
            flash('No está autorizado para acceder a esta sección','error')
            return redirect(url_for('home_bp.dashboard'))    
    pass     

@trackers_bp.route('/')
def home():
    trackers = Tracker.query.all()
    return render_template(
        'trackers/index.html',        
        segment = 'trackers',
        trackers = trackers,        
        current_user=current_user,        
    )

@trackers_bp.route('/<int:id>')
def detail(id):
    tracker = Tracker.query.get(id)
    if tracker:
        return render_template(
            'trackers/detail.html',        
            segment = 'trackers',
            tracker = tracker,
            current_user=current_user,        
        )
    return render_template(
        'trackers/index.html',        
        segment = 'trackers',
     
        current_user=current_user,        
    )

@trackers_bp.route('/delete/<id>')
def delete(id):
    tracker = Tracker.query.get(id)
    tracker.delete()
    flash('Tracker eliminado','success')
    return redirect(url_for('trackers_bp.home'))            

@trackers_bp.route('/commands/<id>',methods=['GET','POST'])
def commands(id):
    if request.method=='POST':
        newCommand = TrackerCommandHistory(tracker_id=request.values.get('tracker_id'),
                                            tracker_command_id=request.values.get('tracker_command_id'),
                                            status='pending')
        try:
            newCommand.create()
            flash('Comando registrado','success')            
        except:
            flash('Ha ocurrido un error','danger')        
        return redirect(url_for('trackers_bp.commands',id=id))     
        
    else:

        tracker = Tracker.query.get(id)
        protocol = TrackerProtocol.query.get(tracker.protocol.id)
        commands = TrackerCommand.query.filter(Tracker.tracker_protocol_id==protocol.id)
        commands_history = TrackerCommandHistory.query.filter(TrackerCommandHistory.tracker_id==id)
        return render_template(
                'trackers/send-command.html',        
                segment = 'trackers',
                commands = commands,        
                tracker = tracker,    
                current_user=current_user,        
                commands_history = commands_history
            )

@trackers_bp.route('/add',methods=['GET','POST'])
def add():
    if request.method=='POST':
        newTracker = Tracker(imei=request.values.get('imei'),
                            phone=request.values.get('phone'),
                            vehicle_id=request.values.get('vehicle_id') or None,
                            tracker_protocol_id=request.values.get('tracker_protocol_id'))
        try:
            newTracker.create()
            flash('Nuevo tracker registrado','success')
            return redirect(url_for('trackers_bp.home'))    
        except:
            flash('Ha ocurrido un error','danger')
            return redirect(url_for('trackers_bp.home'))                                
    else:
        #ignoring the vehicles already asociated to a tracker
        ignore_ids =Tracker.query.with_entities(Tracker.vehicle_id).filter(Tracker.vehicle_id.isnot(None))        
        vehicles = Vehicle.query.filter(Vehicle.id.notin_(ignore_ids))        
        trackers_protocols = TrackerProtocol.query.all()
        return render_template(
            'trackers/add-form.html',        
            segment = 'trackers',
            vehicles = vehicles,
            trackers_protocols = trackers_protocols,
            current_user=current_user,        
        )

@trackers_bp.route('/edit/<id>',methods=['GET','POST'])
def edit(id):
    if request.method=='POST':
        tracker = Tracker.query.get(request.values.get('tracker_id'))
        tracker.phone = request.values.get('phone')
        tracker.vehicle_id = request.values.get('vehicle_id') or None
        
        try:
            tracker.update()
            flash('Datos modificados','success')
            return redirect(url_for('trackers_bp.home'))    
        except:
            flash('Ha ocurrido un error','danger')
            return redirect(url_for('trackers_bp.home'))                                
    else:
        #ignoring the vehicles already asociated to a tracker
        #ignore_ids = [tracker.vehicle_id for tracker in Tracker.query.all()]
        tracker = Tracker.query.get(id)
        ignore_ids =Tracker.query.with_entities(Tracker.vehicle_id).filter(Tracker.vehicle_id.isnot(None))        
        vehicles = []
        if tracker:
            if(tracker.vehicle != None):
                vehicles = Vehicle.query.filter(or_(Vehicle.id==tracker.vehicle_id,Vehicle.id.notin_(ignore_ids)))                       
            else:
                vehicles = Vehicle.query.filter(Vehicle.id.notin_(ignore_ids))
            return render_template(
                'trackers/edit-form.html',        
                segment = 'trackers',
                tracker = tracker,
                vehicles = vehicles,
                current_user=current_user,                
            )
        else:
            flash('Tracker no encontrado','danger')
            return render_template(
                'trackers/index.html',        
                segment = 'trackers',                
                current_user=current_user,                
            )
