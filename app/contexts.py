from collections import OrderedDict
from datetime import datetime

from flask_login import current_user

from flask_security.forms import LoginForm
from sqlalchemy import desc

from app.load_app import app
from app.security import current_user_is_logged
from app.university import Group, Message
from app.university.models.discipline import Discipline


@app.context_processor
def inject_groups():
    groups = Group.active_groups().all()
    return {
        'menu_item_width': 100 / len(groups) if len(groups) else 100,
        'groups': groups
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
def inject_min_cells_count():
    return {
        "min_cells_count": 20
    }


@app.context_processor
def inject_user():
    return {
        "user": current_user,
        "is_logged": current_user_is_logged()
    }


@app.context_processor
def inject_admin():
    data = {}
    message = Message.query.order_by(desc(Message.created_at)).first()
    if current_user_is_logged():
        groups = Group.query.order_by(Group.title).order_by(Group.year, Group.title).all()
        admin_groups = OrderedDict()
        for year in Group.active_years():
            admin_groups[year] = [group for group in groups if group.year == year]

        data = {
            'current_year': Group.current_year(),
            'admin_groups': admin_groups,
            'admin_disciplines': Discipline.query.all(),
        }
    data.update({
        'message': message,
    })
    return data


@app.context_processor
def as_data_attributes():
    def _inner(s, *fields):
        output = []
        for f in fields:
            value = getattr(s, f)
            if isinstance(value, bool):
                value = str(value).lower()
            output.append(u"data-{}=\"{}\"".format(f, value))
        return " ".join(output)
    return dict(as_data_attributes=_inner)