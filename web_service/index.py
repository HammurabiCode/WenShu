from flask import (
    Blueprint
)


bp = Blueprint('index', __name__, url_prefix='/index')

@bp.route('')
def index(): 
    return 'Hello, World Two!'
    
    
@bp.route('hi/<string:username>')
def say_hi(username=''): 
    return 'Hello, {}!'.format(username)
