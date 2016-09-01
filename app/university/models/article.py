import mistune
from sqlalchemy import event

from datetime import datetime
from app.models import BaseMixin, db


class Article(BaseMixin, db.Model):
    title = db.Column(db.String(100))
    menu_title = db.Column(db.String(50))
    text = db.Column(db.String)
    rendered_text = db.Column(db.String)
    discipline_id = db.Column(db.Integer, db.ForeignKey('disciplines.id'))
    visible = db.Column(db.Boolean)

    def __repr__(self):
        return "<Article({title:s} {text:s} {visible:s} {discipline_id:d}>".format(**{
            "title": self.title,
            "text": self.text[:10],
            "visible": "+" if self.visible else "-",
            "discipline_id": self.discipline_id
        })

    @staticmethod
    def before_insert(mapper, connection, target):
        target.created_at = datetime.utcnow()
        target.updated_at = datetime.utcnow()

        if target.text:
            target.rendered_text = mistune.markdown(target.text)



event.listen(Article, 'before_insert', Article.before_insert)
event.listen(Article, 'before_update', Article.before_update)
