import os
import tempfile
from flask import url_for, request
from flask.ext.login import logout_user
from flask.ext.security.utils import encrypt_password, login_user
from flask.ext.security.views import login, logout
from flask.ext.testing import TestCase
from app import db, init_app, cache

from app.load_app import app
from app.security import security, User
from config import BaseConfiguration


class TestConfiguration(BaseConfiguration):
    DEBUG = False

    TESTING = True
    WTF_CSRF_ENABLED = False
    CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class TestCaseBase(TestCase):
    def create_app(self):
        app.config.from_object(TestConfiguration)
        init_app()
        return app

    def setUp(self):
        cache.clear()
        db.init_app(app)
        db.create_all()
        self.user = User.create(email="m", name="m", password=encrypt_password("m"), active=True)

    def tearDown(self):
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
