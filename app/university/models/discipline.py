from sqlalchemy import event

from app.models import BaseMixin, db
from app.storage import Storage


class DisciplineFileStorage(Storage):
    subdir = "disciplines"


class Discipline(BaseMixin, db.Model):
    title = db.Column(db.String(50))
    year = db.Column(db.Integer)
    visible = db.Column(db.Boolean)
    labs = db.relationship("Lab", backref='discipline', order_by="Lab.order", )
    files = db.relationship("DisciplineFile", backref='discipline')
    articles = db.relationship("Article", backref='discipline')

    def __repr__(self):
        return u"<Discipline({id:d}|{title:s}|{visible})>".format(**self.__dict__).encode("utf-8")


event.listen(Discipline, 'before_insert', Discipline.before_insert)
event.listen(Discipline, 'before_update', Discipline.before_update)


class DisciplineFile(BaseMixin, db.Model):
    discipline_id = db.Column(db.Integer, db.ForeignKey('disciplines.id'))
    title = db.Column(db.String(300))
    path = db.Column(db.String)

    @property
    def url(self):
        if self.path:
            return DisciplineFileStorage.url(self.path)
        else:
            return None


event.listen(DisciplineFile, 'before_insert', DisciplineFile.before_insert)
event.listen(DisciplineFile, 'before_update', DisciplineFile.before_update)
