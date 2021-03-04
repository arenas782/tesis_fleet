from flask import Blueprint,render_template
from flask import current_app as app


# Blueprint Configuration
home_bp = Blueprint(
    'home_bp', __name__,url_prefix='/')

@home_bp.route('/')
def home():
    return render_template(
        'index.html',
        
    )