from app.models import BaseMixin, db
from app.university.models.task import Task
from app.university.models.student import Student
from app.university.models.discipline import Discipline
from app.university.models.lab import Lab


class TaskResult(BaseMixin, db.Model):
    done = db.Column(db.Boolean, default=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))

    def __repr__(self):
        return "<TaskResult({id}|{done}|{task_id}<->{student_id})>".format(
            **self.__dict__
        )

    @classmethod
    def get_student_labs(cls, group_id, discipline):
        student_taskresults = {}

        results = TaskResult.query \
            .join(Task).join(Lab).join(Student) \
            .filter(Student.group_id == group_id, Lab.discipline_id == discipline.id)\
            .with_entities(Student.id, Task.id, TaskResult.done)

        for (student_id, task_id, done) in results:
            if student_id not in student_taskresults:
                student_taskresults[student_id] = {}
            if task_id not in student_taskresults[student_id]:
                student_taskresults[student_id][task_id] = done

        tasks = Task.query.filter(Task.lab_id.in_(discipline.labs.with_entities(Lab.id)))

        return student_taskresults, discipline.labs, tasks