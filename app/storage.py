import os

from werkzeug.utils import secure_filename
from flask import request, url_for
from app.load_app import app


class Storage(object):
    subdir = ""

    @classmethod
    def url(cls, filename, full=False):
        url_path = "/uploads/" + os.path.relpath(filename, app.config['UPLOAD_FOLDER'])
        return url_path

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

    @classmethod
    def save(cls, file):
        """
        :param file: form file instance
        :return:
        """
        if file and cls.allowed_file(file.filename):
            filename = secure_filename(file.filename.split('/')[-1])
            save_dir = os.path.join(app.config['UPLOAD_FOLDER'], cls.subdir)
            save_path = os.path.join(save_dir, filename)
            try:
                os.makedirs(save_dir)
            except OSError as ex:
                print ex
            file.save(save_path)
            return save_path
