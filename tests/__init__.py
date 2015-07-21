import os
import shutil

from flask import url_for, request
from flask.ext.security.utils import encrypt_password
from flask.ext.testing import TestCase

import config
from config import BaseConfiguration


class TestConfiguration(BaseConfiguration):
    DEBUG = False

    # TESTING = True
    WTF_CSRF_ENABLED = False
    CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    UPLOAD_FOLDER = os.path.join(BaseConfiguration.BASE_DIR, 'tests', 'public')


# change current app config to test
config.current_config = TestConfiguration

from app.load_app import app
from app.security import User
from app.university import Student
from app import db, init_app, cache


class TestCaseBase(TestCase):
    def create_app(self):
        # app.config.from_object(TestConfiguration)
        init_app()
        return app

    def setUp(self):
        cache.clear()
        db.init_app(app)
        db.create_all()
        self.user = User.create(email="m", name="m", password=encrypt_password("m"), active=True)

    def tearDown(self):
        try:
            shutil.rmtree(app.config['UPLOAD_FOLDER'])
        except OSError:
            pass
        db.session.remove()
        db.drop_all()

    @staticmethod
    def login(func):
        def _wrapper(self=None):
            with self.client:
                self.client.post('login', data={
                    "email": 'm',
                    "password": 'm'
                })
                func(self)
                self.client.post(url_for("security.logout"))

        return _wrapper

    @staticmethod
    def guest_cant(func):
        def _wrapper(self=None):
            with self.client:
                response = func(self)
                self.assertRedirects(response, url_for("security.login", next=request.path))

        return _wrapper

    @property
    def test_image_path(self):
        return os.path.join(app.config['BASE_DIR'], 'tests', 'test_image.jpg')


class TestStorage(TestCaseBase):
    def test_set_file_field(self):
        student = Student()
        student.photo = "cool"
        db.session.add(student)
        db.session.commit()
