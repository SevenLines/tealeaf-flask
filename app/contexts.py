from datetime import datetime
from flask.ext.login import current_user
from flask.ext.security.forms import LoginForm
from app.load_app import app
from app.security import current_user_is_logged
from app.university import Group
from app.university.models.discipline import Discipline


@app.context_processor
def inject_groups():
    groups = Group.active_groups()
    return {
        'menu_item_width': 100 / groups.count() if groups.count() else 100,
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
def inject_now():
    return {
        "now": datetime.now()
    }


@app.context_processor
def inject_user():
    return {
        "user": current_user,
        "is_logged": current_user_is_logged()
    }


@app.context_processor
def inject_admin():
    if current_user_is_logged():
        groups = Group.query.order_by(Group.title).all()
        admin_groups = {}
        for year in Group.active_years():
            admin_groups[year] = [group for group in groups if group.year == year]

        return {
            'current_year': Group.current_year(),
            'admin_groups': admin_groups,
            'admin_disciplines': Discipline.query.all(),
        }
    return {}

