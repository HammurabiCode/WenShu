from flask import Blueprint
from flask_restful import Resource


bp = Blueprint('douban_quato', __name__, url_prefix='/douban')


class Quota(Resource):

    urls = ['/quota']

    def get(self):
        return {'quota': 'ok'}
