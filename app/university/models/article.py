import mistune
import re

from flask.helpers import url_for
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
    deleted = db.Column(db.Boolean)

    def __repr__(self):
        return "<Article({title:s} {text:s} {visible:s} {discipline_id:d}>".format(**{
            "title": self.title,
            "text": self.text[:10],
            "visible": "+" if self.visible else "-",
            "discipline_id": self.discipline_id
        })

    @property
    def safe_title(self):
        return self.title

    @staticmethod
    def before_update(mapper, connection, target):
        if target.text:
            target.rendered_text = mistune.markdown(target.text)

            def callback(match):
                title = match.group('title')
                try:
                    article = Article.filter(title=title).first()
                    return url_for('university.article', article_id=article.pk)
                except:
                    return ""

            target.rendered_text = re.sub('\[article\:(?P<title>.*?)\]', callback, target.rendered_text)

    @staticmethod
    def before_insert(mapper, connection, target):
        target.created_at = datetime.utcnow()
        target.updated_at = datetime.utcnow()

        if target.text:
            target.rendered_text = mistune.markdown(target.text)


event.listen(Article, 'before_insert', Article.before_insert)
event.listen(Article, 'before_update', Article.before_update)
