from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms.validators import DataRequired, InputRequired
from app.university.models.lesson import Lesson

LessonEditForm = model_form(Lesson, base_class=Form,
                            exclude_fk=True,
                            exclude=['created_at', 'updated_at', 'marks'],
                            field_args={
                                'date': {
                                    'format': '%Y-%m-%d'
                                },
                            })

LessonCreateForm = model_form(Lesson, base_class=Form, exclude_fk=False,
                              exclude=['created_at', 'updated_at', 'marks'],
                              field_args={
                                  'date': {
                                      'format': '%Y-%m-%d'
                                  },
                                  'discipline_id': {
                                      'validators': [DataRequired(),]
                                  },
                                  'group_id': {
                                      'validators': [DataRequired(),]
                                  }
                              })
