from datetime import datetime
from flask.ext.login import UserMixin
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import text, func
from sqlalchemy.ext.declarative.api import declarative_base, declared_attr
from app.load_app import app

db = SQLAlchemy(app)


class BaseMixin(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + "s"

    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    #
    @staticmethod
    def before_insert(mapper, connection, target):
        target.created_at = datetime.utcnow()
        target.updated_at = datetime.utcnow()

    @staticmethod
    def before_update(mapper, connection, target):
        target.updated_at = datetime.utcnow()

    @classmethod
    def create(cls, commit=True, **kwargs):
        instance = cls(**kwargs)
        return instance.save(commit=commit)

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    # We will also proxy Flask-SqlAlchemy's get_or_44
    # for symmetry
    @classmethod
    def get_or_404(cls, id):
        return cls.query.get_or_404(id)

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()


class Setting(BaseMixin, db.Model):
    active_year = db.Column(db.SmallInteger, default=datetime.today().year)

    @classmethod
    def instance(cls):
        """

        :return: Setting
        """
        setting = Setting.query.first()
        if not setting:
            setting = Setting.create()
        return setting

