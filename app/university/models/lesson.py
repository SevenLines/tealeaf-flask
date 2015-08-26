# coding=utf-8
from sqlalchemy import event
from app.models import BaseMixin, db
import mistune


class Lesson(BaseMixin, db.Model):
    description = db.Column(db.String)
    date = db.Column(db.DateTime)
    lesson_type = db.Column(db.Integer)
    discipline_id = db.Column(db.Integer, db.ForeignKey('disciplines.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    score_ignore = db.Column(db.Boolean)
    marks = db.relationship("Mark", backref='lesson', lazy='dynamic')

    LESSON_TYPE_PRACTICE = 1
    LESSON_TYPE_TEST = 2
    LESSON_TYPE_LECTION = 3
    LESSON_TYPE_LAB = 4
    LESSON_TYPE_EXAM = 5

    LESSON_TYPES = {
        LESSON_TYPE_PRACTICE: {"name": u"Практика", "cls": ""},
        LESSON_TYPE_TEST: {"name": u"Контрольная", "cls": "test"},
        LESSON_TYPE_LECTION: {"name": u"Лекция", "cls": "lect"},
        LESSON_TYPE_LAB: {"name": u"Лабораторная", "cls": "laba"},
        LESSON_TYPE_EXAM: {"name": u"Экзамен", "cls": "exam"}
    }

    @property
    def style(self):
        type = Lesson.LESSON_TYPES.get(self.lesson_type, None)
        if not type:
            return ""
        return type["cls"]

    @property
    def description_rendered(self):
        return mistune.markdown(self.description, hard_wrap=True)

    def __repr__(self):
        return u"<Lesson({description:s} {date}|{discipline_id:d} lt:{lesson_type:d} si:{score_ignore:s}>" \
            .format(**{
            "date": self.date,
            "lesson_type": self.lesson_type,
            "description": self.description,
            "discipline_id": self.discipline_id,
            "score_ignore": "+" if self.score_ignore else "-",
        }).encode("utf-8")


event.listen(Lesson, 'before_insert', Lesson.before_insert)
event.listen(Lesson, 'before_update', Lesson.before_update)
