from flask import Blueprint
from flask import current_app as app


# Blueprint Configuration
drivers_bp = Blueprint(
    'drivers_bp', __name__,url_prefix='/drivers')

@drivers_bp.route('/')
def home():
    return 'hello'