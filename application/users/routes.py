from flask import Blueprint,render_template,redirect,url_for,request,flash
from flask import current_app as app
from .. import login_manager
from ..utils import role_required   
from ..models import User
from flask_login import login_required, logout_user, current_user, login_user, logout_user

# Blueprint Configuration
users_bp = Blueprint(
    'users_bp', __name__,url_prefix='/users')


@users_bp.before_request
@login_required
def before_request():
    for user_role in current_user.roles:
        if (user_role.name=='admin'):
            pass
        else:
            flash('No está autorizado para acceder a esta sección')
            return redirect(url_for('home_bp.dashboard'))    
    pass 

@users_bp.route('/')
def home():
    users = User.query.all()
    return render_template(
        'users/index.html',        
        segment = 'users',
        users = users,
        current_user=current_user,        
    )

@users_bp.route('/<id>')
def profile(id):
    user = User.query.get(id)
    return render_template(
        'users/profile.html',        
        segment = 'users',
        user = user,
        current_user=current_user,        
    )


@users_bp.route('edit/<id>',methods=['GET','POST'])
def edit(id):
    user = User.query.get(id)        
    if(request.method=="POST"):
        user= User.query.get(request.values.get('user_id'))
        user.name=request.values.get('name')
        user.lastname=request.values.get('lastname')
        user.phone=request.values.get('phone') or None
        user.email=request.values.get('email')        
        password = request.values.get('password')
        password_confirm = request.values.get('password_confirm')
        if password and password_confirm:
            if password_confirm == password:
                user.set_password(password)
                flash('Password actualizada','success')
        user.update()
        flash('Datos modificados','success')
        return redirect(url_for('users_bp.home'))    
    else:                
        return render_template(
            'users/edit-form.html',            
            user = user,
            segment = 'users',                
            current_user = current_user
        )   

