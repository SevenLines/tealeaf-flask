from sqlalchemy import event

from app.models import BaseMixin, db


class Task(BaseMixin, db.Model):
    complexity = db.Column(db.Integer)
    description = db.Column(db.String)
    order = db.Column(db.Integer)
    ignore = db.Column(db.Boolean)
    lab_id = db.Column(db.Integer, db.ForeignKey('labs.id'))

    UNDEFINED = 0
    EASY = UNDEFINED + 1
    MEDIUM = UNDEFINED + 2
    HARD = UNDEFINED + 3
    NIGHTMARE = UNDEFINED + 4

    COMPLEX_CHOICES = {
        UNDEFINED: "",
        EASY: "easy",
        MEDIUM: "medium",
        HARD: "hard",
        NIGHTMARE: "nightmare",
    }

    @property
    def style(self):
        return self.COMPLEX_CHOICES.get(self.complexity, "")


event.listen(Task, 'before_insert', Task.before_insert)
event.listen(Task, 'before_update', Task.before_update)
