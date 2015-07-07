from flask import Blueprint

university = Blueprint('university', __name__)

import app.university.controllers
import app.university.forms