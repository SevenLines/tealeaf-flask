from flask import render_template, abort
from jinja2 import TemplateNotFound
from app.university import university


@university.route('/')
def index():
    return render_template('university/index.html')
