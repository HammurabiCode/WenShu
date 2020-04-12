import os
import importlib
from pkgutil import walk_packages
from flask import Flask, Blueprint
from flask_restful import Resource, Api


def init_app():
    app = Flask('WenShu')
    path = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.basename(os.path.abspath(__file__))

    pkg_name = os.path.basename(path)
    for _, module_name, is_pkg in walk_packages([path], prefix=pkg_name+'.'):
        if module_name.endswith(file_name.split('.')[0]):
            continue
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
            app.register_blueprint(bp)
    return app


web_app = init_app()
