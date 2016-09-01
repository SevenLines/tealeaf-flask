# Import flask and template operators
from flask import render_template
from flask_assets import Environment
from flask_wtf import CsrfProtect
from flask_debugtoolbar import DebugToolbarExtension

from app.admin import admin
from app.contexts import *
from app.logs import *
from app.cache import *
from load_app import app
from app.security import security
from app.models import db
from app.university import university


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403


def init_app():
    CsrfProtect(app)
    toolbar = DebugToolbarExtension(app)

    app.jinja_env.lstrip_blocks = True
    app.jinja_env.trim_blocks = True

    # webassets
    assets_env = Environment(app)

    # Import a module / component using its blueprint handler variable (mod_auth)
    # from app.mod_auth.controllers import mod_auth as auth_module

    # Register blueprint(s)
    app.register_blueprint(university)
