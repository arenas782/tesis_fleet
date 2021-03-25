from flask import Blueprint,render_template,redirect,url_for,request,flash
from flask import current_app as app
from .. import login_manager
from ..models import Vehicle,db,Maintenance,MaintenanceComment
from ..utils import role_required   
from sqlalchemy import and_,or_
from flask_login import login_required, logout_user, current_user, login_user, logout_user
from datetime import date

# Blueprint Configuration
maintenance_bp = Blueprint(
    'maintenance_bp', __name__,url_prefix='/maintenance')

@maintenance_bp.before_request
@login_required
def before_request():    
    if (current_user.role.name=='admin' or current_user.role.name=='taller'):
        pass
    else:
        flash('No está autorizado para acceder a esta sección','error')
        return redirect(url_for('home_bp.dashboard'))    
    

@maintenance_bp.route('/')
def home():
    rows_per_page = 5
    page = request.args.get('page', 1, type=int)
    query = request.args.get('query')

    if query:        
        maintenances = Maintenance.query.join(Vehicle).filter(Vehicle.plate.like('%'+query+'%')).order_by(Maintenance.created_at.desc()).paginate(page=page,per_page=rows_per_page)    
        
    else:        
        maintenances = Maintenance.query.order_by(Maintenance.created_at.desc()).paginate(page=page,per_page=rows_per_page)
    return render_template(
        'maintenance/index.html',                
        maintenances = maintenances,
        current_user=current_user,        
        segment = 'maintenance'
    )

@maintenance_bp.route('/add',methods=['GET','POST'])
def add():
    if request.method=='POST':
        newMaintenance = Maintenance(maintenance_type=request.values.get('maintenance_type'),                            
                            vehicle_id=request.values.get('vehicle_id')
                            )
        comment = request.values.get('comment')

        newMaintenance.comments.append(MaintenanceComment(comment=comment))
        newMaintenance.create()
        
        flash('Nuevo mantenimiento registrado','success')                            
        return redirect(url_for('maintenance_bp.home'))                                
    else:

        vehicles = Vehicle.query.all()
        return render_template(
            'maintenance/add-form.html',                
            vehicles = vehicles,
            segment = 'maintenance',
            current_user=current_user,        
        )

@maintenance_bp.route('/<int:id>')
def detail(id):
    maintenance = Maintenance.query.get(id)
    if maintenance:
        comments = MaintenanceComment.query.filter_by(maintenance_id=id).order_by(MaintenanceComment.created_at.desc())
        return render_template(
            'maintenance/detail.html',        
            segment = 'maintenance',
            comments = comments,
            maintenance = maintenance,
            current_user=current_user,        
        )
    else:
        flash('Registro no encontrado','error')
        return redirect(url_for('maintenance_bp.home'))

@maintenance_bp.route('/edit/<id>',methods=['GET','POST'])
def edit(id):
    if request.method=='POST':
        maintenance = Maintenance.query.get(request.values.get('maintenance_id'))
        maintenance.status = request.values.get('status')
        maintenance.maintenance_type= request.values.get('maintenance_type')        
        comment = request.values.get('comment')                
        try:
            if(comment):
                maintenance.comments.append(MaintenanceComment(comment=comment))
            maintenance.update()
            flash('Datos modificados','success')            
        except:
            flash('Ha ocurrido un error','danger')
        return redirect(url_for('maintenance_bp.home'))    

    else:
        
        maintenance = Maintenance.query.get(id)
    
        if maintenance:            
            return render_template(
                'maintenance/edit-form.html',        
                segment = 'maintenance',                
                maintenance = maintenance,
                current_user=current_user,                
            )
        else:
            flash('Registro no encontrado','error')
            return render_template(
                'maintenance/index.html',        
                segment = 'maintenance',                
                current_user=current_user,                
            )

