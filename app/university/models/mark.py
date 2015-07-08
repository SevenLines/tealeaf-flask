from sqlalchemy import event
from app.models import BaseMixin, db


class Mark(BaseMixin, db.Model):
    value = db.Column(db.Integer, default=0)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))

    def __repr__(self):
        return "<Mark({value})>".format(
            value=self.value
        )


event.listen(Mark, 'before_insert', Mark.before_insert)
event.listen(Mark, 'before_update', Mark.before_update)
