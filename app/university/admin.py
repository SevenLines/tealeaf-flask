from app.models import db
from app.admin import admin
from app.admin import BaseModelView
from app.university.models import Discipline
from app.university.models import Group


class DisciplineModelView(BaseModelView):
    column_list = ('title', 'year', 'visible')

admin.add_view(DisciplineModelView(Discipline, db.session))
admin.add_view(BaseModelView(Group, db.session))
