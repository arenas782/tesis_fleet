from flask import Blueprint,render_template,redirect,url_for,request,flash
from flask import current_app as app
from ..models import db, User
from .. import login_manager

from flask_login import login_required, logout_user, current_user, login_user
# Blueprint Configuration
auth_bp = Blueprint(
    'auth_bp', __name__,url_prefix='/auth')

@auth_bp.route('/login',methods=['GET', 'POST'])
def login():
    # Bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('home_bp.dashboard'))
    if request.method=='POST':

        form_email = request.form['email']
        form_password = request.form['password']

        if not form_email or not form_password or '@' not in form_email:
            flash('Ha introducido algun campo no válido')
            return render_template('login.html')    
        
        user = User.query.filter_by(email=form_email).first()
        if user is None:
            flash('Usuario no encontrado')
            return render_template('login.html')    
        else:
            if user and user.check_password(form_password):
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('home_bp.dashboard'))
            flash('Credenciales inválidas')
            return redirect(url_for('auth_bp.login'))

    return render_template('login.html')
    
@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('Debe iniciar sesión para continuar')
    return redirect(url_for('auth_bp.login'))