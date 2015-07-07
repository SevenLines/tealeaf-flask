from sqlalchemy import event
from app.models import BaseMixin, db


class Task(BaseMixin, db.Model):
    complexity = db.Column(db.Integer)
    description = db.Column(db.String)
    order = db.Column(db.Integer)
    lab_id = db.Column(db.Integer, db.ForeignKey('labs.id'))


event.listen(Task, 'before_insert', Task.before_insert)
event.listen(Task, 'before_update', Task.before_update)
