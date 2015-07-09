from fabric.context_managers import cd, prefix
from fabric.operations import run
from fabric.state import env

env.user = 'mick'
env.hosts = ['93.170.123.27']

env.directory = '/home/mick/projects/tealeaf-flask'
env.additional_env = 'source {}/env.sh'.format(env.directory)
env.activate = 'source {}/env/bin/activate'.format(env.directory)


def deploy():
    with cd(env.directory):
        with cd(env.directory):
            run("git pull")
            with prefix(env.activate):
                with prefix(env.additional_env):
                    run("pip install -r requirements.txt")
                    run("python manage.py db upgrade")
        run("sudo restart tealeaf")