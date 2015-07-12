from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form
from app.university.models.lesson import Lesson

LessonEditForm = model_form(Lesson, Form,
                            exclude_fk=True,
                            exclude=['created_at', 'updated_at', 'marks'],
                            field_args={
                                'date': {
                                    'format': '%Y-%m-%d'
                                }
                            })
