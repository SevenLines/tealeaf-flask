from sqlalchemy import event
from app.models import BaseMixin, db


class Lesson(BaseMixin, db.Model):
    description = db.Column(db.String)
    date = db.Column(db.DateTime)
    lesson_type = db.Column(db.Integer)
    discipline_id = db.Column(db.Integer, db.ForeignKey('disciplines.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    score_ignore = db.Column(db.Boolean)

    def __repr__(self):
        return "<Lesson({title:s} {date}|{discipline_id:d} lt:{lesson_type:d} si:{score_ignore:s}>" \
            .format(**{
            "title": self.title,
            "date": self.date,
            "lesson_type": self.lesson_type,
            "discipline_id": self.discipline_id,
            "score_ignore": "+" if self.score_ignore else "-",
        })


event.listen(Lesson, 'before_insert', Lesson.before_insert)
event.listen(Lesson, 'before_update', Lesson.before_update)
