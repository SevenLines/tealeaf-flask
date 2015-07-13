import json
from flask import url_for
from flask.ext.login import current_user
from flask.ext.security import login_user
from app.tests import TestCaseBase
from app.university import Lesson, Student, Mark, Discipline
from app.models import db
from app.university.models.group import Group


class TestIndexView(TestCaseBase):
    def setUp(self):
        super(TestIndexView, self).setUp()
        group = Group.create()

    def test_anyone_can_watch_index(self):
        response = self.client.get(url_for("university.index"))
        self.assert200(response)


class TestGroupMarksViewWithoutDisciplines(TestCaseBase):
    def setUp(self):
        super(TestGroupMarksViewWithoutDisciplines, self).setUp()
        self.group = Group.create(year=2014, title="2222")

    def test_guest_cant_watch_marks_without_any_disciplines(self):
        response = self.client.get(url_for("university.group_marks", group_id=self.group.id))
        self.assertRedirects(response, url_for("university.index"))

    @TestCaseBase.login
    def test_user_cant_watch_marks_without_any_disciplines(self):
        response = self.client.get(url_for("university.group_marks", group_id=self.group.id))
        self.assertRedirects(response, url_for("university.index"))


class TestGroupMarksView(TestCaseBase):
    def setUp(self):
        super(TestGroupMarksView, self).setUp()
        self.group = Group.create(year=2014, title="2222")
        self.discipline_without_lessons = Discipline.create(title="d1")
        self.discipline_with_lesson = Discipline.create(title="d2")

        self.group = Group.create()
        self.student = Student.create(group_id=self.group.id)
        # self.lesson1 = Lesson.create(discipline_id=self.hidden_discipline.id)
        self.lesson2 = Lesson.create(group_id=self.group.id,
                                     discipline_id=self.discipline_with_lesson.id)
        # self.mark1 = Mark.create(lesson_id=self.lesson1.id, student_id=self.student.id)
        self.mark2 = Mark.create(lesson_id=self.lesson2.id, student_id=self.student.id)

    @TestCaseBase.login
    def test_user_can_watch_groups_marks(self):
        response = self.client.get(url_for("university.group_marks", group_id=self.group.id))
        self.assert200(response)

    @TestCaseBase.guest_cant
    def test_guest_cant_see_hidden_discipline(self):
        return self.client.get(url_for("university.group_marks",
                                       group_id=self.group.id,
                                       discipline_id=self.discipline_without_lessons.id
                                       ))

    def test_guest_can_see_visible_discipline(self):
        response = self.client.get(url_for("university.group_marks",
                                           group_id=self.group.id,
                                           discipline_id=self.discipline_with_lesson.id
                                           ))
        self.assert200(response)


class TestLessonApi(TestCaseBase):
    def setUp(self):
        super(TestLessonApi, self).setUp()
        self.lesson = Lesson.create()

    @TestCaseBase.guest_cant
    def test_guest_cant_update_lesson(self):
        return self.client.post(url_for("university.update_lesson", lesson_id=self.lesson.id))

    @TestCaseBase.login
    def test_user_can_update_lesson(self):
        data = {
            'description': "text",
            'date': '2014-10-21',
            'score_ignore': "false",
            'lesson_type': 3
        }

        response = self.client.post(url_for("university.update_lesson", lesson_id=self.lesson.id), data=data)

        self.assert200(response)
        self.assertEqual(self.lesson.description, data['description'])
        self.assertEqual(self.lesson.score_ignore, False)
        self.assertEqual(self.lesson.lesson_type, data['lesson_type'])
        self.assertEqual(self.lesson.date.strftime("%Y-%m-%d"), data['date'])

    @TestCaseBase.login
    def test_user_got_404_if_lesson_not_exists(self):
        data = {
            'description': "text",
            'date': '2014-10-21',
            'score_ignore': "false",
            'lesson_type': 3
        }

        response = self.client.post(url_for("university.update_lesson",
                                            lesson_id=718293719823), data=data)

        self.assert404(response)

    @TestCaseBase.login
    def test_user_got_400_if_provie_wrong_parameters(self):
        data = {
            'description': "text",
            'date': '2014-102-21',  # << this line wrong
            'score_ignore': "false",
            'lesson_type': 3
        }

        response = self.client.post(url_for("university.update_lesson", lesson_id=self.lesson.id), data=data)

        self.assert400(response)

    @TestCaseBase.guest_cant
    def test_guest_cant_delete_lesson(self):
        lesson = Lesson.create()
        return self.client.delete(url_for("university.delete_lesson", lesson_id=lesson.id))

    @TestCaseBase.login
    def test_user_can_delete_lesson(self):
        lesson = Lesson.create()
        response = self.client.delete(url_for("university.delete_lesson", lesson_id=lesson.id))

        self.assertIsNone(Lesson.get(lesson.id))

        self.assert200(response)

    @TestCaseBase.guest_cant
    def test_guest_cant_create_lesson(self):
        return self.client.post(url_for("university.create_lesson"))

    @TestCaseBase.login
    def test_user_can_create_lesson(self):
        discipline = Discipline.create()
        group = Group.create()

        data = {
            'desription': 'description',
            'date': '2015-07-13',
            'lesson_type': Lesson.LESSON_TYPE_EXAM,

        }

        response = self.client.post(url_for("university.create_lesson"), data=data)
        self.assert400(response, "make sure that you cant create lesson without discipline and group")

        data.update({
            'discipline_id': discipline.id,
            'group_id': group.id,
        })

        response = self.client.post(url_for("university.create_lesson"), data=data)
        self.assert200(response)


class TestMarksApi(TestCaseBase):
    def setUp(self):
        super(TestMarksApi, self).setUp()

        self.lesson1 = Lesson.create()
        self.lesson2 = Lesson.create()

        self.student = Student.create()
        self.mark = Mark.create(lesson_id=self.lesson1.id,
                                student_id=self.student.id,
                                value=1)

    @TestCaseBase.guest_cant
    def test_guest_cant_save_marks(self):
        return self.client.post(url_for("university.save_marks"), data={
            'marks': []
        })

    @TestCaseBase.login
    def test_user_can_update_marks(self):
        response = self.client.post(url_for("university.save_marks"), data=json.dumps([
            {'lesson_id': self.lesson1.id, 'student_id': self.student.id, 'value': '2'},
            {'lesson_id': self.lesson2.id, 'student_id': self.student.id, 'value': '3'},
        ]), headers=[("Content-Type", "application/json; charset=utf-8"),
                     ('X-Requested-With', 'XMLHttpRequest')])
        self.assert200(response)
        self.assertEqual(self.mark.value, 2)
        self.assertEqual(Mark.query.filter(Mark.student_id == self.student.id,
                                           Mark.lesson_id == self.lesson2.id).first().value, 3)


class TestDisciplinesApi(TestCaseBase):
    def setUp(self):
        super(TestDisciplinesApi, self).setUp()

    @TestCaseBase.guest_cant
    def test_guest_cant_create_discipline(self):
        return self.client.post(url_for("university.discipline_create"))

    @TestCaseBase.guest_cant
    def test_guest_cant_remove_discipline(self):
        discipline = Discipline.create()
        return self.client.post(url_for("university.discipline_delete", discipline_id=discipline.id))

    @TestCaseBase.guest_cant
    def test_guest_cant_update_discipline(self):
        discipline = Discipline.create()
        return self.client.post(url_for("university.discipline_update", discipline_id=discipline.id))

    @TestCaseBase.login
    def test_user_can_create_discipline(self):
        count_before = Discipline.query.count()
        data = {
            'title': "new_discipline"
        }
        response = self.client.post(url_for("university.discipline_create"), data=data)
        self.assertRedirects(response, "/")
        self.assertEqual(count_before + 1, Discipline.query.count())

        d = Discipline.query.first()
        self.assertEqual(d.title, data['title'])

    @TestCaseBase.login
    def test_user_can_remove_discipline(self):
        discipline = Discipline.create()
        self.assertIsNotNone(Discipline.get(discipline.id))
        response = self.client.post(url_for("university.discipline_delete", discipline_id=discipline.id))
        self.assertRedirects(response, "/")
        self.assertIsNone(Discipline.get(discipline.id))

    @TestCaseBase.login
    def test_user_can_update_discipline(self):
        discipline = Discipline.create()
        data = {
            'title': "new_discipline2",
            "year": 2015,
            "visible": True,
        }
        response = self.client.post(url_for("university.discipline_update", discipline_id=discipline.id), data=data)
        self.assertRedirects(response, "/")

        db.session.refresh(discipline)
        self.assertEqual(discipline.title, data['title'])
        self.assertEqual(discipline.year, data['year'])
        self.assertEqual(discipline.visible, data['visible'])


class TestGroupsApi(TestCaseBase):
    @TestCaseBase.guest_cant
    def test_guest_cant_create_group(self):
        return self.client.post(url_for("university.group_create"))

    @TestCaseBase.guest_cant
    def test_guest_cant_remove_group(self):
        group = Group.create()
        return self.client.post(url_for("university.group_delete", group_id=group.id))

    @TestCaseBase.guest_cant
    def test_guest_cant_update_group(self):
        group = Group.create()
        return self.client.post(url_for("university.group_update", group_id=group.id))

    @TestCaseBase.login
    def test_user_can_create_group(self):
        count_before = Group.query.count()
        data = {
            'title': "new_group"
        }
        response = self.client.post(url_for("university.group_create"), data=data)
        self.assertRedirects(response, "/")
        self.assertEqual(count_before + 1, Group.query.count())

        d = Group.query.first()
        self.assertEqual(d.title, data['title'])

    @TestCaseBase.login
    def test_user_can_remove_group(self):
        group = Group.create()
        self.assertIsNotNone(Group.get(group.id))
        response = self.client.post(url_for("university.group_delete", group_id=group.id))
        self.assertRedirects(response, "/")
        self.assertIsNone(Group.get(group.id))

    @TestCaseBase.login
    def test_user_can_update_group(self):
        group = Group.create()
        data = {
            'title': "new_group2",
            "year": 2015,
        }
        response = self.client.post(url_for("university.group_update", group_id=group.id), data=data)
        self.assertRedirects(response, "/")

        db.session.refresh(group)
        self.assertEqual(group.title, data['title'])
        self.assertEqual(group.year, data['year'])
