from app.load_app import app
from app.university import Group


@app.context_processor
def inject_groups():
    groups = Group.active_groups()
    return {
        'menu_item_width': 100 / groups.count(),
        'groups': groups.all()
    }
