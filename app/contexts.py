from app.load_app import app
from app.university import Group


@app.context_processor
def inject_groups():
    groups = Group.query.all()
    return {
        'menu_item_width': 100 / Group.query.count(),
        'groups': groups
    }
