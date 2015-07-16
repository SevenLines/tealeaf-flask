from sqlalchemy import event
from app.models import BaseMixin, db


class Lab(BaseMixin, db.Model):
    title = db.Column(db.String(50))
    description = db.Column(db.String)
    discipline_id = db.Column(db.Integer, db.ForeignKey('disciplines.id'))
    visible = db.Column(db.Boolean)
    regular = db.Column(db.Boolean)
    tasks = db.relationship("Task")

    def __repr__(self):
        return u"<Lab({title:s}|{discipline_id:d} v:{visible:s} r:{visible:s}>".format(**{
            "title": self.title,
            "discipline_id": self.discipline_id,
            "visible": "+" if self.visible else "-",
            "regular": "+" if self.regular else "-",
        }).encode("utf-8")


event.listen(Lab, 'before_insert', Lab.before_insert)
event.listen(Lab, 'before_update', Lab.before_update)
