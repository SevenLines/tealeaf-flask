from datetime import datetime

import mistune
import re

from flask import url_for
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy import text, func
from sqlalchemy.ext.declarative.api import declarative_base, declared_attr
from app.load_app import app

db = SQLAlchemy(app)


class BaseMixin(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + "s"

    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    #
    @staticmethod
    def before_insert(mapper, connection, target):
        target.created_at = datetime.utcnow()
        target.updated_at = datetime.utcnow()

    @staticmethod
    def before_update(mapper, connection, target):
        target.updated_at = datetime.utcnow()

    @classmethod
    def create(cls, commit=True, **kwargs):
        instance = cls(**kwargs)
        return instance.save(commit=commit)

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    # We will also proxy Flask-SqlAlchemy's get_or_44
    # for symmetry
    @classmethod
    def get_or_404(cls, id):
        return cls.query.get_or_404(id)

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()


class Setting(BaseMixin, db.Model):
    active_year = db.Column(db.SmallInteger, default=datetime.today().year)

    @classmethod
    def instance(cls):
        """

        :return: Setting
        """
        setting = Setting.query.first()
        if not setting:
            setting = Setting.create()
        return setting


class Message(BaseMixin, db.Model):
    message = db.Column(db.Text, default="")
    rendered_message = db.Column(db.Text, default="")

    @staticmethod
    def before_insert(mapper, connection, target):
        target.created_at = datetime.utcnow()
        target.updated_at = datetime.utcnow()

        if target.message:
            target.rendered_message = mistune.markdown(target.message)

            def callback(match):
                title = match.group('title')
                text = match.group('text')
                try:
                    from app.university import Article
                    article = Article.query.filter(Article.title==title).first()
                    url = url_for('university.article', article_id=article.id, slug=article.title)
                    return u'<a href="{}">{}</a>'.format(url, text)
                except:
                    return ""

            target.rendered_message = re.sub('\\((?P<text>.*?)\)\[article\:(?P<title>.*?)\]', callback, target.rendered_message)


event.listen(Message, 'before_insert', Message.before_insert)
event.listen(Message, 'before_insert', Message.before_insert)

event.listen(Setting, 'before_insert', Setting.before_insert)
event.listen(Setting, 'before_insert', Setting.before_insert)