from flask import render_template, request, redirect, url_for
from flask.ext.login import current_user, login_url
from flask.views import View
from app.security import current_user_is_logged

from app.university import university
from app.university.models import *


class IndexView(View):
    def dispatch_request(self):
        template = "university/index.html"
        if request.headers.get('X-Pjax', None):
            template = "university/_charts.html"
        return render_template(template)


# class GroupView(View):
#     def dispatch_request(self, group_id):
#         group = Group.query.get(group_id)
#         discipline_id = request.cookies.get('discipline_id', None)
#         if not discipline_id:
#             discipline_id = Discipline.query.first().id
#         return redirect(url_for("university.group_marks", group_id=group.id, discipline_id=discipline_id))
#

class GroupMarksView(View):
    """
    renders marks table for specified discipline and group
    """

    def dispatch_request(self, group_id, discipline_id=None):
        group = Group.query.get(group_id)

        discipline_id = request.cookies.get('discipline_id', None)
        if not discipline_id:
            discipline_id = Discipline.query.first().id

        if current_user_is_logged():
            disciplines = Discipline.query
        else:
            disciplines = group.disciplines

        discipline = disciplines.filter(Discipline.id == discipline_id).first()

        # if not discipline and user is not logged then redirect
        if not discipline and not current_user_is_logged():
            return redirect(url_for('security.login', next=request.url))

        # fetch all data from database, form marks table
        students = group.students.all()
        students_marks = {}
        lessons = Lesson.query.filter(Lesson.group_id == group.id).order_by(Lesson.date).all()
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
            for lesson in lessons:
                points, percents = student.points(students_marks[student.id]['marks'], lessons)
                students_marks[student.id]['points'] = points
                students_marks[student.id]['percents'] = percents

        template = "university/group.html"
        if request.headers.get('X-Pjax', None):
            template = "university/_marks.html"

        return render_template(
            template,
            group=group,
            discipline=discipline,
            students_marks=students_marks,
            students=students,
            lessons=lessons,
            lesson_types=Lesson.LESSON_TYPES,
            marks_types=Mark.MARKS,
            disciplines=disciplines.all(),
        )


university.add_url_rule('/', view_func=IndexView.as_view('index'))
university.add_url_rule('/g/<int:group_id>/', view_func=GroupMarksView.as_view('group'))
university.add_url_rule('/g/<int:group_id>/m/<int:discipline_id>/',
                        view_func=GroupMarksView.as_view('group_marks'),
                        defaults={'discipline_id': None})
