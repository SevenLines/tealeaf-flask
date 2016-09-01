from fabric.context_managers import cd, prefix
from fabric.operations import run, local
from fabric.state import env

env.user = 'mmailm_hosting'
env.hosts = ['193.106.92.221']

env.directory = '/var/www/home/hosting_mmailm/projects/tealeaf-flask'
env.additional_env = 'source {}/env.sh'.format(env.directory)
env.activate = 'source {}/env/bin/activate'.format(env.directory)
env.use_ssh_config=True

def build_assets():
    try:
        local("python manage.py assets --parse-templates build")
        try:
            local("git commit -a -m 'build assets'")
        except:
            pass

        try:
            local("git checkout master")
            local("git merge --no-ff develop")
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
                run(". .env")
                run("pip install -r requirements.txt")
                run("python manage.py db upgrade")