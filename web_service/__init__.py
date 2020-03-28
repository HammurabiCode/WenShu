from flask import Flask
from web_service import index


web_app = Flask('WenShu')
web_app.register_blueprint(index.bp)
