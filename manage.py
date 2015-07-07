from flask import url_for
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from app import app, db

# -=-=-=-=-=-=-=-=-=-=-=-=-
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


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
if __name__ == '__main__':
    manager.run()
