from datetime import datetime
from flask.ext.login import UserMixin
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import text, func
from sqlalchemy.ext.declarative.api import declarative_base, declared_attr

db = SQLAlchemy()


class BaseMixin(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()+"s"

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
