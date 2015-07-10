from datetime import datetime
from sqlalchemy import text, event
from app.models import db, BaseMixin
from app.university.models.lesson import Lesson
from app.university.models.mark import Mark


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

    def points(self, marks, lessons):
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

        max = lessons_count * 3
        min = lessons_count * -2
        base = 0.3
        percents_sum = base
        if points_sum == 0:
            percents_sum = base
        elif points_sum > 0:
            percents_sum = base + (float(points_sum) / max) * (1 - base)
        else:
            percents_sum = base - (float(points_sum) / min) * base

        return points_sum, int(percents_sum * 100)


event.listen(Student, 'before_insert', Student.before_insert)
event.listen(Student, 'before_update', Student.before_update)
