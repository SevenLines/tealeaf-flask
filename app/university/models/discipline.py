from sqlalchemy import event
from app.models import BaseMixin, db


class Discipline(BaseMixin, db.Model):
    title = db.Column(db.String(50))
    year = db.Column(db.Integer)
    visible = db.Column(db.Boolean)
    labs = db.relationship("Lab", lazy="dynamic")

    def __repr__(self):
        return u"<Discipline({id:d}|{title:s}|{visible})>".format(**self.__dict__).encode("utf-8")


event.listen(Discipline, 'before_insert', Discipline.before_insert)
event.listen(Discipline, 'before_update', Discipline.before_update)
