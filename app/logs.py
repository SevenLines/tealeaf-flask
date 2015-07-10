import os
from app import app
from logging import FileHandler

if not app.debug:
    import logging

    file_handler = FileHandler(app.config['LOG_PATH'], 'a+', encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)
