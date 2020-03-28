from flask import (
    Blueprint
)


bp = Blueprint('index', __name__, url_prefix='/index')

@bp.route('')
def index(): 
    return 'Hello, World!'