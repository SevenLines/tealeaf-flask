from datetime import datetime

from sqlalchemy import event

from app.models import db, BaseMixin, Setting
from app.university.models.taskresult import TaskResult
from app.university.models.task import Task
from app.university.models.lab import Lab
from app.university.models.student import Student
from app.university.models.mark import Mark
from app.university.models.lesson import Lesson
from app.university.models.discipline import Discipline


class Group(BaseMixin, db.Model):
    title = db.Column(db.String(20))
    year = db.Column(db.SmallInteger)
    captain_id = db.Column(db.Integer)
    students = db.relationship("Student", backref='group', lazy='dynamic', order_by=Student.second_name)

    @staticmethod
    def current_year(now=datetime.now()):
        """
        :return: current learning year
        """
        # if now.month < 9:  # if not september yet
        #     return now.year - 1
        # return now.year
        return [2014, 2016, 2017]  # [Setting.instance().active_year]

    def __repr__(self):
        return u"<Group({id:d}|{year:d}|{title:s})>".format(**self.__dict__).encode("utf-8")

    @classmethod
    def active_groups(cls):
        return Group.query.filter(Group.year.in_(Group.current_year())).order_by(Group.year, Group.title)

    @classmethod
    def active_years(cls):
        years = [year[0] for year in db.session.query(Group.year).order_by(Group.year).distinct().all()]
        if len(years):
            return range(min(years) - 1, max(years) + 2)
        return []

    @property
    def girls(self):
        return self.students.filter(Student.sex == 0)

    @property
    def boys(self):
        return self.students.filter(Student.sex == 1)

    @property
    def disciplines(self):
        lesson_discipline = Lesson.query \
            .join(Discipline) \
            .filter(Lesson.group_id == self.id) \
            .with_entities(Discipline).distinct()

        tasks_discipline = TaskResult.query \
            .join(Student) \
            .join(Task) \
            .join(Lab) \
            .join(Discipline) \
            .filter(Student.group_id == self.id) \
            .with_entities(Discipline).distinct()

        return lesson_discipline.union(tasks_discipline)

    def marks(self, value=None, only_positive=False):
        out_marks = Mark.query.filter(Mark.student_id.in_(self.students.with_entities(Student.id)))
        if only_positive:
            out_marks = out_marks.filter(Mark.value >= 0)
        if value is not None:
            out_marks = out_marks.filter(Mark.value == value)
        return out_marks

    @staticmethod
    def before_insert(mapper, connection, target):
        target.created_at = datetime.utcnow()
        target.updated_at = datetime.utcnow()

        if target.year is None:
            target.year = Group.current_year()[0]


event.listen(Group, 'before_insert', Group.before_insert)
event.listen(Group, 'before_insert', Group.before_insert)
