# coding=utf-8
from flask import url_for, request, abort
from flask.ext.admin.base import Admin
from flask.ext.admin.contrib import sqla
from flask.ext.admin.contrib.sqla.view import ModelView
from flask.ext.login import current_user
from flask.ext.security.decorators import roles_required
from werkzeug.utils import redirect
from app.load_app import app
from app.models import db
from app.security import User, Role


class BaseModelView(sqla.ModelView):
    @roles_required("superuser")
    def is_accessible(self):
        if not current_user.is_active() or not current_user.is_authenticated():
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated():
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


admin = Admin(app, name=u"Админка")
admin.add_view(BaseModelView(User, db.session))
admin.add_view(BaseModelView(Role, db.session))
