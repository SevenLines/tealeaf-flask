# Import flask and template operators
from flask import render_template

from flask.ext.assets import Environment, ManageAssets
from flask.ext.script import Manager
from app.admin import admin
from flask_debugtoolbar import DebugToolbarExtension

from app.contexts import *
from app.security import security
from app.logs import *
from load_app import app
from app.models import db

db.init_app(app)
security.init_app(app)
admin.init_app(app)
toolbar = DebugToolbarExtension(app)

app.jinja_env.lstrip_blocks = True
app.jinja_env.trim_blocks = True


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403


# webassets
assets_env = Environment(app)
# assets_env.config['cache'] = app.config['ASSETS_CACHE']
# assets_env.config['manifest'] = app.config['ASSETS_MANIFEST']
# assets_env.config['auto_build'] = app.config['ASSETS_AUTO_BUILD']


# Import a module / component using its blueprint handler variable (mod_auth)
# from app.mod_auth.controllers import mod_auth as auth_module
from app.university import university

# Register blueprint(s)
app.register_blueprint(university)
# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
# db.create_all()
