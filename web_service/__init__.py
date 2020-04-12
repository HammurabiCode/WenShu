import os
import importlib
from pkgutil import walk_packages
from flask import Flask, Blueprint
from flask_restful import Resource, Api
from web_service import index

path = os.path.dirname(os.path.abspath(__file__))
pkg_name = os.path.basename(path)

web_app = Flask('WenShu')

for _, module_name, is_pkg in walk_packages([path], prefix=pkg_name+'.'):
    module = importlib.import_module(module_name)
    bp, resources = None, []
    for k in dir(module):
        v = getattr(module, k)
        if isinstance(v, Blueprint):
            bp = v
        if isinstance(v, type(Resource)) and 'urls' in dir(v):
            resources.append(v)
            pass
    if bp:
        if resources:
            api = Api(bp)
            for x in resources:
                urls = getattr(x, 'urls')
                api.add_resource(x, *urls)
        web_app.register_blueprint(bp)

