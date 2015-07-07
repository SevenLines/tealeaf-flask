from flask import Blueprint

university = Blueprint('university', __name__)

from app.university.models import *
from app.university.controllers import *
