from app.models import BaseMixin, db


class TaskResult(BaseMixin, db.Model):
    done = db.Column(db.Boolean, default=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
