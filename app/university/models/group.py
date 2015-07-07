from sqlalchemy import event
from app.models import db, BaseMixin


class Group(BaseMixin, db.Model):
    title = db.Column(db.String(20))
    year = db.Column(db.SmallInteger)
    captain_id = db.Column(db.Integer)
    students = db.relationship("Student", backref='group', lazy='dynamic')

    def __repr__(self):
        return "<Group(title={title:s}, year={year:d}>".format(**self.__dict__)

event.listen(Group, 'before_insert', Group.before_insert)
event.listen(Group, 'before_update', Group.before_update)

