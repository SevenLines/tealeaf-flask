from flask import render_template
from flask.views import View

from app.university import university


class IndexView(View):
    def dispatch_request(self):
        return render_template('university/index.html')


university.add_url_rule('/', view_func=IndexView.as_view('index'))
