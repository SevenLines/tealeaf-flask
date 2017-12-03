# coding=utf-8
from itertools import groupby
from operator import or_
from pprint import pformat

from flask import render_template, request, redirect, url_for, Response
from flask_login import login_required
from flask.helpers import make_response
from flask.views import View, MethodView
from flask_security.views import login
from sqlalchemy import desc, case

from sqlalchemy.orm import joinedload, contains_eager

from datetime import datetime
from app.cache import cache
from app.models import Message
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
    for (discipline_id,) in Discipline.query.with_entities(Discipline.id).all():
        cache.delete(cache_key_for_students_marks(group_id, discipline_id))


def reset_student_marks_cache_for_discipline_id(discipline_id):
    for (group_id,) in Group.query.with_entities(Group.id).all():
        cache.delete(cache_key_for_students_marks(group_id, discipline_id))


class IndexView(View):
    def dispatch_request(self):
        template = "university/index.html"
        if request.headers.get('X-Pjax', None):
            template = "university/_charts.html"

        marks = Mark.query.join(Student, Group).filter(
            Group.year == Group.current_year()
        ).with_entities(
            Mark.value,
            Group.id.label("group_id"),
            Student.id.label("student_id"),
            Student.sex
        ).order_by("group_id", "value", "sex")

        marks = {
            groupd_id: {
                "marks": {
                    v: {
                        "marks_count": len(marks),
                        "marks_summ": sum(i.value if i.value <= Mark.MARK_INCREDIBLE else 1 for i in marks)
                    }
                    for v, marks in {v: list(marks) for v, marks in groupby(items, lambda x: x.value)}.items()
                    if Mark.MARK_ABSENT <= v <= Mark.MARK_INCREDIBLE or v == Mark.MARK_SHINING
                },
                "marks_count": len(items),
                "marks_count_positive": len(list(i for i in items if Mark.MARK_BASE < i.value <= Mark.MARK_INCREDIBLE)),
                "marks_summ": sum(i.value for i in items),
                "marks_summ_positive": sum(i.value for i in items if Mark.MARK_BASE < i.value <= Mark.MARK_INCREDIBLE)
            }
            for groupd_id, items in {id: list(items) for id, items in groupby(marks, lambda x: x.group_id)}.items()
        }

        for group_id, info in marks.items():
            info['max_summ'] = max(i['marks_summ'] for i in info['marks'].values())

        return render_template(template, **{
            'marks': marks,
        })


@university.route("/g/<int:group_id>/m/<int:discipline_id>/<slug>")
@university.route("/g/<int:group_id>/<slug>")
@university.route("/g/<int:group_id>/")
def group_marks(group_id, slug=None, discipline_id=None):
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

    discipline = disciplines.filter(Discipline.id == discipline_id)\
        .options(joinedload('labs'), joinedload('files'), joinedload('articles')).first()
    if discipline is None:
        discipline = disciplines.first()

    # if not discipline and user is not logged then redirect
    if not discipline and not current_user_is_logged():
        return redirect(url_for('security.login', next=request.path))

    if group.year != Group.current_year() and not current_user_is_logged():
        return redirect(url_for('security.login', next=request.path))

    def make_cache_key():
        return cache_key_for_students_marks(group.id, discipline.id)

    def get_all_data(group, discipline):
        lessons = Lesson.query.filter(Lesson.group_id == group.id)\
            .filter(Lesson.discipline_id == discipline.id) \
            .order_by(Lesson.date, Lesson.id).all()

        students = group.students\
            .outerjoin(Student.marks)\
            .options(contains_eager(Student.marks))\
            .filter(or_(Mark.lesson_id == None, Mark.lesson_id.in_([i.id for i in lessons]))).all()

        labs = discipline.labs

        students_info = {}
        for student in students:
            student_info = {
                'marks': {},
                'tasks': {},
                'points': 0,
                'percents': 0,
            }
            students_info[student.id] = student_info
            for mark in student.marks:
                student_info['marks'][mark.lesson_id] = mark

            for task in student.tasks:
                student_info['tasks'][task.task_id] = task

            student_info['points'], student_info['percents'] \
                = student.points(student_info['marks'],
                                 lessons,
                                 sum([len(lab.tasks) for lab in labs if lab.regular and lab.visible]),
                                 len(student_info['tasks']))

        return {
            'students': students,
            'lessons': lessons,
            'labs': labs,
            'students_info': students_info
        }

    data = get_all_data(group, discipline)

    template = "university/group.html"
    if request.headers.get('X-Pjax', None):
        template = "university/_marks.html"

    response = make_response(render_template(
        template,
        group=group,
        discipline=discipline,

        students=data['students'],
        lessons=data['lessons'],
        labs=data['labs'],
        articles=[a for a in discipline.articles if a.visible or current_user_is_logged()],
        disciplines=disciplines.order_by(Discipline.title).all(),
        has_visible_labs=len([lab for lab in data['labs'] if lab.visible]) > 0,

        students_info=data['students_info'],

        lesson_types=Lesson.LESSON_TYPES,
        marks_types=Mark.MARKS,
    ))

    response.set_cookie('discipline_id', str(discipline_id))

    return response


class SetMessage(MethodView):
    @login_required
    def post(self):
        data = request.form
        m = Message.create(message=data.get('message'))
        return redirect(request.headers['REFERER'])


class SetSetting(MethodView):
    @login_required
    def post(self):
        key = request.form['key']
        value = request.form['value']
        s = Setting.instance()
        setattr(s, key, value)
        s.save()

        return redirect(request.headers['REFERER'])


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


class SaveTaskResults(MethodView):
    @login_required
    def post(self):
        tasks_results = request.get_json()
        for result in tasks_results:
            r = TaskResult.query.filter(TaskResult.student_id == result['student_id'],
                                        TaskResult.task_id == result['task_id']).first()
            if r is None:
                r = TaskResult(
                    student_id=result['student_id'],
                    task_id=result['task_id']
                )
                db.session.add(r)
            if not result['done']:
                r.delete(commit=False)

        db.session.commit()

        return Response()


@university.route('/lesson/<int:lesson_id>/', methods=['POST', ])
@login_required
def update_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)

    form = LessonEditForm(request.form, lesson)
    if form.validate_on_submit():
        populate(form, lesson)
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
        populate(form, lesson)
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
        populate(form, discipline)
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
        populate(form, discipline)
        discipline.update()
        if request.is_xhr:
            return Response()
        return redirect(request.referrer or "/")
    if request.is_xhr:
        return Response(pformat(form.errors), status=400)
    return redirect(request.referrer or "/")


@university.route("/discipline/<int:discipline_id>/file/", methods=['POST', ])
@login_required
def discipline_file_create(discipline_id):
    discipline = Discipline.get_or_404(discipline_id)
    form = DisciplineFileForm(request.form)
    if form.validate_on_submit():
        discipline_file = DisciplineFile()

        populate(form, discipline_file)
        discipline_file.path = DisciplineFileStorage.save(request.files['file'])

        if discipline_file.path is None:
            return redirect(request.referrer or "/")

        discipline_file.discipline_id = discipline_id
        if not discipline_file.title:
            discipline_file.title = request.files['file'].filename

        db.session.add(discipline_file)
        db.session.commit()
        if request.is_xhr:
            return Response()
        return redirect(request.referrer or "/")
    if request.is_xhr:
        return Response(pformat(form.errors), status=400)
    return redirect(request.referrer or "/")


@university.route("/discipline_file/<int:discipline_file_id>/d/", methods=['POST', ])
@login_required
def discipline_file_delete(discipline_file_id):
    discipline_file = DisciplineFile.get_or_404(discipline_file_id)
    discipline_file.delete()
    if request.is_xhr:
        return Response()
    return redirect(request.referrer or "/")


@university.route("/article/<int:article_id>/", methods=['GET', ])
@university.route("/article/<int:article_id>/<slug>", methods=['GET', ])
def article(article_id, slug=None):
    a = Article.get_or_404(article_id)
    if not current_user_is_logged() and not a.visible:
        return redirect(url_for('security.login', next=request.path))

    response = make_response(render_template(
        "university/_article.html",
        article=a,
        discipline=discipline,
    ))

    return response


@university.route("/article/<int:article_id>/", methods=['POST', ])
@university.route("/article/<int:article_id>/<slug>", methods=['POST', ])
@login_required
def article_update(article_id,  slug=None):
    a = Article.get_or_404(article_id)

    form = ArticleForm(request.form, a)
    if form.validate_on_submit():
        populate(form, a)
        a.update()
        if request.is_xhr:
            return Response()
        return redirect(request.referrer or "/")

    if request.is_xhr:
        return Response(pformat(form.errors), status=400)
    return redirect(request.referrer or "/")


@university.route("/article/<int:article_id>/toggle-hide", methods=['GET', ])
@login_required
def article_toggle_hide(article_id):
    a = Article.get_or_404(article_id)

    a.visible = not a.visible
    a.save()

    if request.is_xhr:
        return Response()
    return redirect(request.referrer or "/")

@university.route("/article/", methods=['POST', ])
@login_required
def article_create():
    form = ArticleForm(request.form)
    if form.validate_on_submit():
        a = Article()

        populate(form, a)
        db.session.add(a)
        if not a.title:
            a.title = u'новая статья от {}'.format(datetime.now())

        db.session.commit()

        return redirect(url_for('university.article', article_id=a.id))

    return redirect(request.referrer or "/")


@university.route("/article/<int:article_id>/d/", methods=['POST', ])
@login_required
def article_delete(article_id):
    article = Article.get_or_404(article_id)
    article.delete()
    if request.is_xhr:
        return Response()
    return redirect(request.referrer or "/")


@university.route("/group/", methods=['POST', ])
@login_required
def group_create():
    form = GroupForm(request.form)
    if form.validate_on_submit():
        group = Group()
        populate(form, group)
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
        populate(form, group)
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
        populate(form, student)

        if 'photo' in request.files:
            student.photo = StudentStorage.save(request.files['photo'])

        db.session.add(student)
        db.session.commit()

        if student.group_id:
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
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        assert isinstance(form, Form)

        populate(form, student)

        if "photo" in request.files:
            student.photo = StudentStorage.save(request.files['photo'])
        elif "remove_photo" in request.form:
            student.photo = None

        if student.group_id:
            reset_student_marks_cache_for_group_id(student.group_id)

        student.update()
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

    if student.group_id:
        reset_student_marks_cache_for_group_id(group_id)

    if request.is_xhr:
        return Response()
    return redirect(request.referrer or "/")


@university.route("/lab/<int:lab_id>/", methods=['POST'])
@login_required
def lab_edit(lab_id):
    lab = Lab.get_or_404(lab_id)
    data = request.get_json()
    lab.visible = data['visible']
    lab.description = data['description']
    lab.title = data['title']
    lab.update()
    if request.is_xhr:
        return Response()
    return redirect(request.referrer or "/")


@university.route("/task/<int:task_id>/", methods=['POST'])
@login_required
def lab_task_edit(task_id):
    task = Task.get_or_404(task_id)
    data = request.get_json()
    task.description = data['description']
    task.update()
    if request.is_xhr:
        return Response()
    return redirect(request.referrer or "/")


@university.route("/lab/set-tasks-order/", methods=['POST'])
@login_required
def update_lab_tasks_order():
    data = request.get_json()
    order_ids = data['order']
    order = [(Task.id == task_id, index) for index, task_id in enumerate(order_ids)]
    db.session.query(Task).filter(Task.id.in_(order_ids)).update({
        'order': case(order, else_=-1)
    }, synchronize_session=False)
    db.session.commit()

    if request.is_xhr:
        return Response()
    return redirect(request.referrer or "/")

university.add_url_rule('/marks/', view_func=SaveMarks.as_view('save_marks'),
                        methods=['POST', ])
university.add_url_rule('/tasks-results/', view_func=SaveTaskResults.as_view('save_task_results'),
                        methods=['POST', ])
university.add_url_rule('/', view_func=IndexView.as_view('index'))
university.add_url_rule('/message/', view_func=SetMessage.as_view('set_message'), methods=['POST', ])
university.add_url_rule('/settting/', view_func=SetSetting.as_view('set_setting'), methods=['POST', ])
