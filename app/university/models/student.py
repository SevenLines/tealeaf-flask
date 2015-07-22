# coding=utf-8
import os

from sqlalchemy import event

from sqlalchemy.orm.attributes import get_history

from app.models import db, BaseMixin
from app.storage import Storage
from app.university.models.lesson import Lesson
from app.university.models.mark import Mark


class StudentStorage(Storage):
    subdir = "students"


class Student(BaseMixin, db.Model):
    name = db.Column(db.String)
    second_name = db.Column(db.String)
    sex = db.Column(db.SmallInteger)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    email = db.Column(db.String)

    photo = db.Column(db.String)

    @property
    def photo_url(self):
        if self.photo:
            return StudentStorage.url(self.photo)
        return ""

    @staticmethod
    def before_update(mapper, connection, target):
        # remove old photo
        old_photo_path = get_history(target, 'photo')
        if old_photo_path.has_changes():
            if len(old_photo_path[2]) and old_photo_path[2][0]:
                os.remove(old_photo_path[2][0])
        # continue with base method
        return BaseMixin.before_update(mapper, connection, target)

    def __repr__(self):
        return u"<Student({id:d}|{name:s} {second_name:s}, {sex:s} из группы {group:s})>".format(**{
            "id": self.id,
            "name": self.name,
            "second_name": self.second_name,
            "sex": u"девушка" if self.sex == 0 else u"парень",
            "group": self.group.title
        }).encode('utf8')

    def points(self, marks, lessons, tasks_count=0, tasks_done=0):
        points_sum = 0
        lessons_count = 0
        for lesson in lessons:
            if not lesson.score_ignore:
                lessons_count += 1

            if lesson.lesson_type == Lesson.LESSON_TYPE_EXAM:
                continue

            mark = marks.get(lesson.id, None)
            if mark:
                if mark.value == Mark.MARK_BLACK_HOLE:
                    if points_sum > 0:
                        points_sum = 0
                elif mark.value == Mark.MARK_SHINING:
                    if points_sum < lessons_count * 3:
                        points_sum = lessons_count * 3
                elif mark.value == Mark.MARK_MERCY:
                    if points_sum < 0:
                        points_sum = 0
                elif mark.value == Mark.MARK_KEEP:
                    pass
                elif mark.value:
                    points_sum += mark.value

        max = lessons_count * 3 + tasks_count
        min = lessons_count * -2
        base = 0.3

        points_sum += tasks_done

        if points_sum == 0:
            percents_sum = base
        elif points_sum > 0:
            percents_sum = base + (float(points_sum) / max) * (1 - base)
        else:
            percents_sum = base - (float(points_sum) / min) * base

        return points_sum, int(percents_sum * 100)


event.listen(Student, 'before_insert', Student.before_insert)
event.listen(Student, 'before_update', Student.before_update)
