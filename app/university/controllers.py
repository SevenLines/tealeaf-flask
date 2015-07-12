from flask import render_template, request, redirect, url_for, Response, abort
from flask.ext.login import current_user, login_url, login_required
from flask.views import View, MethodView
from app.cache import cache
from app.security import current_user_is_logged

from app.university import university
from app.university.forms import LessonEditForm
from app.university.models import *


def cache_key_for_students_marks(group_id, discipline_id):
    return "cache|group:{group_id}|discipline:{discipline_id}".format(
        group_id=group_id,
        discipline_id=discipline_id
    )


class IndexView(View):
    def dispatch_request(self):
        template = "university/index.html"
        if request.headers.get('X-Pjax', None):
            template = "university/_charts.html"
        return render_template(template)


class GroupMarksView(View):
    """
    renders marks table for specified discipline and group
    """

    def dispatch_request(self, group_id, discipline_id=None):
        group = Group.query.get_or_404(group_id)

        if not discipline_id:
            discipline_id = request.cookies.get('discipline_id', None)
            if not discipline_id:
                discipline = Discipline.query.first()
                if discipline:
                    discipline_id = discipline.id
                else:
                    return redirect(url_for("university.index"))

        if current_user_is_logged():
            disciplines = Discipline.query
        else:
            disciplines = group.disciplines

        discipline = disciplines.filter(Discipline.id == discipline_id).first()

        # if not discipline and user is not logged then redirect
        if not discipline and not current_user_is_logged():
            return redirect(url_for('security.login', next=request.path))

        def make_cache_key():
            return cache_key_for_students_marks(group.id, discipline.id)

        @cache.cached(key_prefix=make_cache_key)
        def get_student_marks(group, discipline):
            # fetch all data from database, form marks table
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

        students, lessons, students_marks = get_student_marks(group, discipline)

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


class SaveMarks(MethodView):
    @login_required
    def post(self):
        marks = request.get_json()
        for mark in marks:
            m = Mark.query.filter(Mark.student_id == mark['student_id'], Mark.lesson_id == mark['lesson_id']).first()
            if m is None:
                m = Mark(
                    student_id=mark['student_id'],
                    lesson_id=mark['lesson_id']
                )
                db.session.add(m)
            m.value = mark['value']

        # reset cache
        for lesson in Lesson.query.filter(Lesson.id.in_([m['lesson_id'] for m in marks])).all():
            cache.delete(cache_key_for_students_marks(lesson.group_id, lesson.discipline_id))

        db.session.commit()

        return Response()


@university.route('/lesson/<int:lesson_id>/', methods=['POST', ])
@login_required
def update_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)

    form = LessonEditForm(request.form, lesson)
    if form.validate():
        form.populate_obj(lesson)
        lesson.update()
        cache.delete(cache_key_for_students_marks(lesson.group_id, lesson.discipline_id))
        return Response()

    # reset cache

    return Response(status=400)


university.add_url_rule('/', view_func=IndexView.as_view('index'))
university.add_url_rule('/marks/', view_func=SaveMarks.as_view('save_marks'),
                        methods=['POST', ])

university.add_url_rule('/g/<int:group_id>/', view_func=GroupMarksView.as_view('group'))
university.add_url_rule('/g/<int:group_id>/m/<int:discipline_id>/',
                        view_func=GroupMarksView.as_view('group_marks'))
