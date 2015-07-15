from pprint import pprint, pformat
from flask import render_template, request, redirect, url_for, Response, abort
from flask.ext.login import current_user, login_url, login_required
from flask.helpers import make_response
from flask.views import View, MethodView
from app.cache import cache
from app.security import current_user_is_logged

from app.university import university
from app.university.forms import *
from app.university.models import *


def cache_key_for_students_marks(group_id, discipline_id):
    return "cache|group:{group_id}|discipline:{discipline_id}".format(
        group_id=group_id,
        discipline_id=discipline_id
    )


def reset_student_marks_cache_for_group_id(group_id):
    group = Group.get(group_id)
    for (discipline_id,) in group.disciplines.with_entities(Discipline.id).all():
        cache.delete(cache_key_for_students_marks(group_id, discipline_id))


def reset_student_marks_cache_for_discipline_id(discipline_id):
    # discipline = Discipline.get(discipline_id)
    for (group_id,) in Group.query.with_entities(Group.id).all():
        cache.delete(cache_key_for_students_marks(group_id, discipline_id))


class IndexView(View):
    def dispatch_request(self):
        template = "university/index.html"
        if request.headers.get('X-Pjax', None):
            template = "university/_charts.html"
        return render_template(template)


@university.route("/g/<int:group_id>/m/<int:discipline_id>/")
@university.route("/g/<int:group_id>/")
def group_marks(group_id, discipline_id=None):
    group = Group.query.get_or_404(group_id)

    if current_user_is_logged():
        disciplines = Discipline.query
    else:
        disciplines = group.disciplines

    if not discipline_id:
        discipline_id = request.cookies.get('discipline_id', None)
        if not discipline_id:
            discipline = disciplines.first()
            if discipline:
                discipline_id = discipline.id
            else:
                return redirect(url_for("university.index"))

    discipline = disciplines.filter(Discipline.id == discipline_id).first()
    if discipline is None:
        discipline = disciplines.first()

    # if not discipline and user is not logged then redirect
    if not discipline and not current_user_is_logged():
        return redirect(url_for('security.login', next=request.path))

    def make_cache_key():
        return cache_key_for_students_marks(group.id, discipline.id)

    students, lessons, students_marks = cache.cached(key_prefix=make_cache_key)(
        Mark.get_student_marks)(group, discipline)

    template = "university/group.html"
    if request.headers.get('X-Pjax', None):
        template = "university/_marks.html"

    response = make_response(render_template(
        template,
        group=group,
        discipline=discipline,
        students_marks=students_marks,
        students=students,
        lessons=lessons,
        lesson_types=Lesson.LESSON_TYPES,
        marks_types=Mark.MARKS,
        disciplines=disciplines.order_by(Discipline.title).all(),
    ))

    response.set_cookie('discipline_id', str(discipline_id))

    return response


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
    if form.validate_on_submit():
        form.populate_obj(lesson)
        lesson.update()
        cache.delete(cache_key_for_students_marks(lesson.group_id, lesson.discipline_id))
        return Response()

    return Response(status=400)


@university.route('/lesson/<int:lesson_id>/', methods=['DELETE', ])
@login_required
def delete_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)

    cache.delete(cache_key_for_students_marks(lesson.group_id, lesson.discipline_id))

    lesson.delete()
    return Response()


@university.route('/lesson/', methods=['POST', ])
@login_required
def create_lesson():
    form = LessonCreateForm(request.form)
    if form.validate_on_submit():
        lesson = Lesson()
        form.populate_obj(lesson)
        lesson.save()

        cache.delete(cache_key_for_students_marks(lesson.group_id, lesson.discipline_id))
        return Response()

    return Response(pformat(form.errors), status=400)


@university.route("/discipline/", methods=['POST', ])
@login_required
def discipline_create():
    form = DisciplineForm(request.form)
    if form.validate_on_submit():
        discipline = Discipline()
        form.populate_obj(discipline)
        db.session.add(discipline)
        db.session.commit()
        if request.is_xhr:
            return Response()
        return redirect(request.referrer or "/")
    if request.is_xhr:
        return Response(pformat(form.errors), status=400)
    return redirect(request.referrer or "/")


@university.route("/discipline/<int:discipline_id>/d/", methods=['POST', ])
@login_required
def discipline_delete(discipline_id):
    discipline = Discipline.get_or_404(discipline_id)
    discipline.delete()
    if request.is_xhr:
        return Response()
    return redirect(request.referrer or "/")


@university.route("/discipline/<int:discipline_id>/u/", methods=['POST', ])
@login_required
def discipline_update(discipline_id):
    discipline = Discipline.get_or_404(discipline_id)
    form = DisciplineForm(request.form, discipline)
    if form.validate_on_submit():
        form.populate_obj(discipline)
        discipline.update()
        if request.is_xhr:
            return Response()
        return redirect(request.referrer or "/")
    if request.is_xhr:
        return Response(pformat(form.errors), status=400)
    return redirect(request.referrer or "/")


@university.route("/group/", methods=['POST', ])
@login_required
def group_create():
    form = GroupForm(request.form)
    if form.validate_on_submit():
        group = Group()
        form.populate_obj(group)
        db.session.add(group)
        db.session.commit()
        if request.is_xhr:
            return Response()
        return redirect(request.referrer or "/")
    if request.is_xhr:
        return Response(pformat(form.errors), status=400)
    return redirect(request.referrer or "/")


@university.route("/group/<int:group_id>/u/", methods=['POST', ])
@login_required
def group_update(group_id):
    group = Group.get_or_404(group_id)
    form = GroupForm(request.form, group)
    if form.validate_on_submit():
        form.populate_obj(group)
        group.update()
        if request.is_xhr:
            return Response()
        return redirect(request.referrer or "/")
    if request.is_xhr:
        return Response(pformat(form.errors), status=400)
    return redirect(request.referrer or "/")


@university.route("/group/<int:group_id>/d/", methods=['POST', ])
@login_required
def group_delete(group_id):
    group = Group.get_or_404(group_id)
    group.delete()
    if request.is_xhr:
        return Response()
    return redirect(request.referrer or "/")


@university.route("/student/", methods=['POST', ])
@login_required
def student_create():
    form = StudentForm(request.form)
    if form.validate_on_submit():
        student = Student()
        form.populate_obj(student)
        db.session.add(student)
        db.session.commit()

        reset_student_marks_cache_for_group_id(student.group_id)

        if request.is_xhr:
            return Response()
        return redirect(request.referrer or "/")
    if request.is_xhr:
        return Response(pformat(form.errors), status=400)
    return redirect(request.referrer or "/")


@university.route("/student/<int:student_id>/u/", methods=['POST', ])
@login_required
def student_update(student_id):
    student = Student.get_or_404(student_id)
    form = StudentForm(request.form, student)
    if form.validate_on_submit():
        form.populate_obj(student)
        student.update()

        reset_student_marks_cache_for_group_id(student.group_id)

        if request.is_xhr:
            return Response()
        return redirect(request.referrer or "/")
    if request.is_xhr:
        return Response(pformat(form.errors), status=400)
    return redirect(request.referrer or "/")


@university.route("/student/<int:student_id>/d/", methods=['POST', ])
@login_required
def student_delete(student_id):
    student = Student.get_or_404(student_id)
    group_id = student.group_id
    student.delete()

    reset_student_marks_cache_for_group_id(group_id)

    if request.is_xhr:
        return Response()
    return redirect(request.referrer or "/")


university.add_url_rule('/marks/', view_func=SaveMarks.as_view('save_marks'),
                        methods=['POST', ])
university.add_url_rule('/', view_func=IndexView.as_view('index'))
