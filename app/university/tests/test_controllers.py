from flask import url_for
from flask.ext.login import current_user
from flask.ext.security import login_user
from app.tests import TestCaseBase
from app.university import Lesson
from app.models import db


class TestLessonApi(TestCaseBase):
    def setUp(self):
        super(TestLessonApi, self).setUp()

        self.lesson = Lesson()
        db.session.add(self.lesson)
        db.session.commit()

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
