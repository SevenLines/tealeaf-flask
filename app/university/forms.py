from flask_wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms.validators import DataRequired

from app.models import db
from app.university.models.article import Article
from app.university.models.lab import Lab
from app.university.models.student import Student
from app.university.models.group import Group
from app.university.models.discipline import Discipline, DisciplineFile
from app.university.models.lesson import Lesson


def populate(form, obj):
    assert isinstance(form, Form)
    assert isinstance(obj, db.Model)
    for key, value in form._fields.items():
        data = value.object_data if len(value.raw_data) == 0 else value.data
        if hasattr(obj, key):
            setattr(obj, key, data)


StudentForm = model_form(Student, base_class=Form, exclude_fk=False,
                         only=['name', 'sex', 'second_name', 'group_id', 'email', 'photo'],
                         field_args={
                         })

ArticleForm = model_form(Article, base_class=Form, exclude_fk=False,
                         exclude=['discipline'],
                         field_args={
                             'discipline_id': {
                                 'validators': [DataRequired(), ]
                             },
                         })

DisciplineForm = model_form(Discipline, base_class=Form,
                            only=['title', 'year', 'visible', 'regular'],
                            )

DisciplineFileForm = model_form(DisciplineFile, base_class=Form,
                                exclude=['discipline'],
                                field_args={
                                    'file': {
                                        'validators': [DataRequired(), ]
                                    },
                                })

GroupForm = model_form(Group, base_class=Form,
                       exclude=['created_at', 'updated_at', 'students'],
                       field_args={
                           'year': {
                               'validators': [DataRequired(), ]
                           },
                       })

LessonEditForm = model_form(Lesson, base_class=Form,
                            exclude_fk=True,
                            exclude=['created_at', 'updated_at', 'marks', 'discipline'],
                            field_args={
                                'date': {
                                    'format': '%Y-%m-%d'
                                },
                            })

LessonCreateForm = model_form(Lesson, base_class=Form, exclude_fk=False,
                              exclude=['created_at', 'updated_at', 'marks', 'discipline'],
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

LabEditForm = model_form(Lab, base_class=Form, exclude_fk=True,
                         exclude=['order', 'created_at', 'updated_at', 'tasks', 'discipline' ])