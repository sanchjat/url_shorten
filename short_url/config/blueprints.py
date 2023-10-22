# -*- coding: utf-8 -*-


def register_blueprints(app):
    '''
    Place your blueprints import here.

    E.g.

    from intiny.catalog.blueprints import catalogs
    app.register_blueprint(catalogs)
    '''
    from short_url.urls import url_apis
    from short_url.users import user_apis
    app.register_blueprint(user_apis.users_blueprint, prefix="/users")
    app.register_blueprint(url_apis.urls_blueprint)

