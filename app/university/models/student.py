from datetime import datetime
from sqlalchemy import text, event
from app import db


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    second_name = db.Column(db.String)
    sex = db.Column(db.Boolean)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    email = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=text('now()'))
    updated_at = db.Column(db.DateTime, server_default=text('now()'))

    @staticmethod
    def before_insert(mapper, connection, target):
        target.created_at = datetime.utcnow()
        target.updated_at = datetime.utcnow()

    @staticmethod
    def before_update(mapper, connection, target):
        target.updated_at = datetime.utcnow()


event.listen(Student, 'before_insert', Student.before_insert)
event.listen(Student, 'before_update', Student.before_update)
