# -*- coding: utf-8 -*-

from flask import Flask


from config.blueprints import register_blueprints

__version__ = '0.1.0'



def create_app(configuration='Production'):
    settings = 'config.settings.%s' % configuration

    app = Flask(__name__)
    app.config.from_object(settings)
    register_blueprints(app)
    return app
