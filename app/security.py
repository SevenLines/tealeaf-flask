from flask_login import LoginManager, current_user
from flask_security import RoleMixin, UserMixin, SQLAlchemyUserDatastore, Security
from sqlalchemy import event
from app.load_app import app
from app.models import db, BaseMixin

# login_manager = LoginManager()

# Define models
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))


class Role(BaseMixin, RoleMixin, db.Model):
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


event.listen(Role, 'before_insert', Role.before_insert)
event.listen(Role, 'before_update', Role.before_update)


class User(BaseMixin, UserMixin, db.Model):
    name = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return "<User({id:d}|{name:s}|{email:s})".format(
            id=self.id,
            name=self.name,
            email=self.email,
        )


def current_user_is_logged():
    return current_user.is_active and current_user.is_authenticated


def current_user_is_superuser():
    return current_user_is_logged() and current_user.has_role("superuser")


event.listen(User, 'before_insert', User.before_insert)
event.listen(User, 'before_update', User.before_update)

user_data_store = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, datastore=user_data_store)
