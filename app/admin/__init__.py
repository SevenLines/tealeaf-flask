# coding=utf-8
from flask import url_for, request, abort
from flask_admin.base import Admin
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla.view import ModelView
from flask_login import current_user
from flask_security.decorators import roles_required
from werkzeug.utils import redirect
from app.load_app import app
from app.models import db
from app.security import User, Role, current_user_is_logged, current_user_is_superuser


class BaseModelView(sqla.ModelView):
    # @roles_required("superuser")
    def is_accessible(self):
        if not current_user_is_logged():
            return False

        if not current_user_is_superuser():
            return False

        return True

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
