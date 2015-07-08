from datetime import datetime
from sqlalchemy import text, event
from app.models import db, BaseMixin


class Student(BaseMixin, db.Model):
    name = db.Column(db.String)
    second_name = db.Column(db.String)
    sex = db.Column(db.SmallInteger)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    email = db.Column(db.String)

    def __repr__(self):
        return u"<Student({name:s} {second_name:s} {sex:s} {group_id:d}>".format(**{
            "name": self.name,
            "second_name": self.second_name,
            "sex": "W" if self.sex == 0 else "M",
            "group_id": self.group_id
        }).encode('utf8')


event.listen(Student, 'before_insert', Student.before_insert)
event.listen(Student, 'before_update', Student.before_update)
