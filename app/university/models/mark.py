# coding=utf-8
from sqlalchemy import event
from app.models import BaseMixin, db


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


event.listen(Mark, 'before_insert', Mark.before_insert)
event.listen(Mark, 'before_update', Mark.before_update)
