from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms.validators import DataRequired, InputRequired
from app.university.models.student import Student
from app.university.models.group import Group
from app.university.models.discipline import Discipline
from app.university.models.lesson import Lesson

DisciplineForm = model_form(Discipline, base_class=Form,
                            exclude=['created_at', 'updated_at'])

GroupForm = model_form(Group, base_class=Form,
                       exclude=['created_at', 'updated_at', 'students'])

StudentForm = model_form(Student, base_class=Form,
                         exclude=['created_at', 'updated_at', 'group'])

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
                                      'validators': [DataRequired(), ]
                                  },
                                  'group_id': {
                                      'validators': [DataRequired(), ]
                                  }
                              })
