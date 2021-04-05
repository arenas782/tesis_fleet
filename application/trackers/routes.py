from flask import Blueprint,render_template,redirect,url_for,request,flash
from flask import current_app as app
from .. import login_manager
from ..models import Tracker,Vehicle,db,TrackerProtocol,TrackerCommand,TrackerCommandHistory,TrackerLog
from ..utils import role_required   
from sqlalchemy import and_,or_
from flask_login import login_required, logout_user, current_user, login_user, logout_user
from datetime import date
import sys


# Blueprint Configuration
trackers_bp = Blueprint(
    'trackers_bp', __name__,url_prefix='/trackers')

@trackers_bp.before_request
@login_required
def before_request():    
    if (current_user.role.name=='admin' or current_user.role.name=='operador'):
        pass
    else:
        flash('No está autorizado para acceder a esta sección','error')
        return redirect(url_for('home_bp.dashboard'))    
         

@trackers_bp.route('/')
def home():
    rows_per_page = 15
    page = request.args.get('page', 1, type=int)
    query = request.args.get('query')
    trackers = Tracker.query
    if query:                
        trackers = trackers.filter(Tracker.imei.like('%'+query+'%'))
    else:
        trackers = trackers

    trackers=trackers.order_by(Tracker.created_at.desc()).paginate(page=page,per_page=rows_per_page)
    return render_template(
        'trackers/index.html',        
        segment = 'trackers',
        query = query,
        trackers = trackers,        
        current_user=current_user,        
    )

@trackers_bp.route('/<int:id>')
def detail(id):
    tracker = Tracker.query.get(id)
    if tracker:
        tracker_logs = TrackerLog.query.filter_by(tracker_id=tracker.id).order_by(TrackerLog.date.desc()).limit(5)
        

        last_sent_commands = TrackerCommandHistory.query.filter_by(tracker_id=tracker.id).order_by(TrackerCommandHistory.created_at.desc()).limit(5)

        return render_template(
            'trackers/detail.html',        
            segment = 'trackers',
            tracker = tracker,
            tracker_logs = tracker_logs,
            last_sent_commands = last_sent_commands,
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
    if tracker:
        tracker.delete()
        flash('Tracker eliminado','success')
    else:
        flash('Tracker no encontrado','error')
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

        rows_per_page = 15
        page = request.args.get('page', 1, type=int)
        tracker = Tracker.query.get(id)
        protocol = TrackerProtocol.query.get(tracker.protocol.id)
        commands = TrackerCommand.query.filter(Tracker.tracker_protocol_id==protocol.id)
        commands_history = TrackerCommandHistory.query.filter(TrackerCommandHistory.tracker_id==id).order_by(TrackerCommandHistory.created_at.desc()).paginate(page=page,per_page=rows_per_page)
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

@trackers_bp.route('logs/<id>')
def logs(id):
    tracker = Tracker.query.get(id)
    today = date.today()
    rows_per_page = 15
    page = request.args.get('page', 1, type=int)
    d1 = today.strftime("%Y-%m-%d")
    newdate  = request.args.get('daterange')
    logs = []
    if tracker:    
        if newdate:            
            newdate=newdate.split('-')
            logs = TrackerLog.query.filter_by(tracker_id=tracker.id).filter(TrackerLog.date.between(newdate[0],newdate[1]))
        else:
            logs = TrackerLog.query.filter_by(tracker_id=tracker.id).filter_by(date=d1)
        logs = logs.order_by(TrackerLog.date.desc()).limit(10)
        
        
        
    return render_template(
        'trackers/logs.html',        
        logs = logs,
        query=newdate,
        
        segment = 'trackers',
        tracker = tracker,                
        current_user=current_user,                
    )

@trackers_bp.route('/print_logs')
def print_logs():
    from flask_weasyprint import HTML, render_pdf    
    tracker_id = request.args.get('tracker_id')
    from_date = request.args.get('from')
    to_date = request.args.get('to')
    tracker = Tracker.query.get(tracker_id)
    if tracker:
        logs = TrackerLog.query.filter_by(tracker_id=tracker.id).filter(TrackerLog.date.between(from_date,to_date))
        html = render_template('trackers/pdf_logs.html', logs=logs,tracker=tracker,from_date=from_date,to_date=to_date)
        pdfname=tracker.imei+'.pdf'
        return render_pdf(HTML(string=html))
        #return render_template('trackers/pdf_logs.html', logs=logs,tracker=tracker,from_date=from_date,to_date=to_date)
    else:
        return 'error'

@trackers_bp.route('/maps/<id>')
def maps(id):
    tracker = Tracker.query.get(id)
    if tracker:
        today = date.today()
        d1 = today.strftime("%Y-%m-%d")
        newdate  = request.args.get('daterange')
        markers = []
        if newdate:            
            newdate=newdate.split('-')
            markers = TrackerLog.query.filter_by(tracker_id=tracker.id).filter(TrackerLog.date.between(newdate[0],newdate[1])).order_by(TrackerLog.created_at.desc())
        else:
            markers = TrackerLog.query.filter_by(tracker_id=tracker.id).filter_by(date=d1).order_by(TrackerLog.created_at.desc())

        print (markers.count())
        if markers.count() <1:
            flash('No hay registros para la fecha especificada','error')                
        return render_template(
            'trackers/maps.html',        
            segment = 'trackers',
            markers = markers,
            current_user=current_user,        
        )
            

        
        
        


