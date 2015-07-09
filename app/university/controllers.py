from flask import render_template
from flask.views import View

from app.university import university
from app.university.models import *


class IndexView(View):
    def dispatch_request(self):
        return render_template('university/index.html')


class GroupView(View):
    def dispatch_request(self, group_id):
        group = Group.query.get(group_id)
        return render_template(
            "university/group.html",
            group=group,
            discipline=Discipline.query.first(),
            disciplines=Discipline.query.all(),
        )


university.add_url_rule('/', view_func=IndexView.as_view('index'))
university.add_url_rule('/g/<int:group_id>/', view_func=GroupView.as_view('group'))
