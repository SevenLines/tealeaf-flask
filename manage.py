from getpass import getpass
from flask import url_for
from flask_assets import ManageAssets
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_security.registerable import register_user
from flask_security.utils import encrypt_password
from app import app, db, init_app

# -=-=-=-=-=-=-=-=-=-=-=-=-
from app.security import user_data_store, User, Role

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command("assets", ManageAssets())


# -=-=-=-=-=-=-=-=-=-=-=-=-
# list routes command
@manager.command
def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)

    for line in sorted(output):
        print line


# -=-=-=-=-=-=-=-=-=-=-=-=-
# create_user command
@manager.command
def create_user():
    username = raw_input("Enter name:")
    email = raw_input("Enter email:")
    password = getpass("Enter password:")
    password_repeat = getpass("Enter password once more:")
    if password != password_repeat:
        print("Passwords not equivalent!")

    # user = create_user(name=username, email=email, password=password)
    user = user_data_store.create_user(name=username, email=email, password=encrypt_password(password))
    db.session.commit()
    if user:
        print("User successfully created")


# -=-=-=-=-=-=-=-=-=-=-=-=-
# create_user command
@manager.command
def create_superuser():
    def get_superuser_role():
        role = Role.query.filter_by(name="superuser").first()
        if not role:
            role = Role(name="superuser", description="grants full access")
            db.session.add(role)
            db.session.commit()
        return role

    username = raw_input("Enter name:")
    email = raw_input("Enter email:")
    password = getpass("Enter password:")
    password_repeat = getpass("Enter password once more:")
    if password != password_repeat:
        print("Passwords not equivalent!")

    user = user_data_store.create_user(name=username, email=email, password=encrypt_password(password))
    user.roles.append(get_superuser_role())
    db.session.commit()
    if user:
        print("User successfully created")


# -=-=-=-=-=-=-=-=-=-=-=-=-
if __name__ == '__main__':
    init_app()
    manager.run()
