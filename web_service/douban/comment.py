from flask import Blueprint
from flask_restful import Resource


bp = Blueprint('douban_comment', __name__, url_prefix='/douban')


class Comment(Resource):

    urls = ['/comment']

    def get(self):
        return {'comment': 'ok'}
