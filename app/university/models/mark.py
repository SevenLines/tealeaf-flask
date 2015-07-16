# coding=utf-8
from sqlalchemy import event
from app.models import BaseMixin, db
from app.university.models.lesson import Lesson


class Mark(BaseMixin, db.Model):
    value = db.Column(db.Integer, default=0)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))

    MARK_BASE = 0
    MARK_SPECIAL = 1000

    MARK_BLACK_HOLE = MARK_BASE - (MARK_SPECIAL + 1)
    MARK_ABSENT = MARK_BASE - 2
    MARK_EMPTY = MARK_BASE
    MARK_NORMAL = MARK_BASE + 1
    MARK_GOOD = MARK_BASE + 2
    MARK_EXCELLENT = MARK_BASE + 3
    MARK_AWESOME = MARK_BASE + 4
    MARK_FANTASTIC = MARK_BASE + 5
    MARK_INCREDIBLE = MARK_BASE + 6
    MARK_SHINING = MARK_BASE + (MARK_SPECIAL + 1)
    MARK_MERCY = MARK_BASE + (MARK_SPECIAL + 2)
    MARK_KEEP = MARK_BASE + (MARK_SPECIAL + 3)

    MARKS = {
        MARK_BLACK_HOLE: u'black-hole',
        MARK_ABSENT: u'absent',
        MARK_EMPTY: u'empty',  # без оценки
        MARK_NORMAL: u'normal',
        MARK_GOOD: u'good',
        MARK_EXCELLENT: u'excellent',
        MARK_AWESOME: u'awesome',
        MARK_FANTASTIC: u'fantastic',
        MARK_INCREDIBLE: u'incredible',
        MARK_SHINING: u'shining',
        MARK_MERCY: u'mercy',
    }

    @property
    def style(self):
        return Mark.MARKS.get(self.value, "")

    def __repr__(self):
        return "<Mark({value})>".format(
            value=self.value
        )

    @staticmethod
    def get_student_lessons(group, discipline):
        """
        fetch all data from database, form marks table
        :param group: Group instance
        :param discipline: Discipline instance
        :return: (students, lessons, students_marks)
        """
        students_marks = {}

        students = group.students.all()
        lessons = Lesson.query.filter(Lesson.group_id == group.id, Lesson.discipline_id == discipline.id) \
            .order_by(Lesson.date).all()

        for student in students:
            students_marks[student.id] = {
                'marks': {}
            }
            for lesson in lessons:
                students_marks[student.id]['marks'][lesson.id] = None

        marks = Mark.query.filter(Mark.lesson_id.in_([l.id for l in lessons])).all()
        for m in marks:
            students_marks[m.student_id]['marks'][m.lesson_id] = m

        for student in students:
            points, percents = student.points(students_marks[student.id]['marks'], lessons)
            students_marks[student.id]['points'] = points
            students_marks[student.id]['percents'] = percents
        return students, lessons, students_marks


event.listen(Mark, 'before_insert', Mark.before_insert)
event.listen(Mark, 'before_update', Mark.before_update)
