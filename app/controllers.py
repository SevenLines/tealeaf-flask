import os

from flask import request, Response, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.wsgi import SharedDataMiddleware

from app.load_app import app

app.add_url_rule('/uploads/<filename>', 'uploaded_file', build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads':  app.config['UPLOAD_FOLDER']
})