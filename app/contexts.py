from flask.ext.login import current_user
from flask.ext.security.forms import LoginForm
from app.load_app import app
from app.security import current_user_is_logged
from app.university import Group


@app.context_processor
def inject_groups():
    groups = Group.active_groups()
    return {
        'menu_item_width': 100 / groups.count(),
        'groups': groups.all()
    }


@app.context_processor
def inject_login_form():
    if not current_user_is_logged():
        return {
            "login_user_form": LoginForm()
        }
    return {}


@app.context_processor
def inject_user():
    return {
        "user": current_user,
        "is_logged": current_user_is_logged()
    }
