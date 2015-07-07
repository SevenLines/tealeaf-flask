# Import flask and template operators
from flask import Flask, render_template
from flask.ext.assets import Environment

# Import SQLAlchemy
import flask
from flask.ext.sqlalchemy import SQLAlchemy


# Configurations

app = Flask(__name__)
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
from app.models import db

db.init_app(app)


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# webassets
assets = Environment()
assets.init_app(app)


# Import a module / component using its blueprint handler variable (mod_auth)
# from app.mod_auth.controllers import mod_auth as auth_module
from app.university import university

# Register blueprint(s)
app.register_blueprint(university, url_prefix="/university")
# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
# db.create_all()
