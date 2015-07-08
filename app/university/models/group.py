from sqlalchemy import event
from app.models import db, BaseMixin
from app.university.models.student import Student
from app.university.models.mark import Mark


class Group(BaseMixin, db.Model):
    title = db.Column(db.String(20))
    year = db.Column(db.SmallInteger)
    captain_id = db.Column(db.Integer)
    students = db.relationship("Student", backref='group', lazy='dynamic')

    def __repr__(self):
        return u"<Group(title={title:s}, year={year:d}>".format(**self.__dict__).encode("utf8")

    @classmethod
    def active_groups(cls):
        return Group.query.filter(Group.year == 2014)

    @property
    def girls(self):
        return self.students.filter(Student.sex == 0)

    @property
    def boys(self):
        return self.students.filter(Student.sex == 1)

    def marks(self, value):
        out_marks = Mark.query.filter(Mark.student_id.in_(self.students.with_entities(Student.id)))
        if value:
            out_marks = out_marks.filter(Mark.value == value)
        return out_marks


event.listen(Group, 'before_insert', Group.before_insert)
event.listen(Group, 'before_update', Group.before_update)
