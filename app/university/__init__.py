from flask import Blueprint

university = Blueprint('university', __name__, static_folder="/static")

from app.university.models import *
from app.university.controllers import *
