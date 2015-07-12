from fabric.context_managers import cd, prefix
from fabric.operations import run, local
from fabric.state import env

env.user = 'mick'
env.hosts = ['93.170.123.27']

env.directory = '/home/mick/projects/tealeaf-flask'
env.additional_env = 'source {}/env.sh'.format(env.directory)
env.activate = 'source {}/env/bin/activate'.format(env.directory)


def build_assets():
    try:
        local("git checkout master")
        local("git merge --no-ff develop")
        local("python manage.py assets --parse-templates build")
        try:
            local("git commit -a -m 'build assets'")
        except:
            pass
    finally:
        local("git checkout develop")

def deploy():
    build_assets()
    local('git push')
    with cd(env.directory):
        run("git stash")
        run("git pull")
        with prefix(env.activate):
            with prefix(env.additional_env):
                run("pip install -r requirements.txt")
                run("python manage.py db upgrade")
        run("sudo restart tealeaf")
