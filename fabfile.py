from fabric.context_managers import cd
from fabric.operations import run
from fabric.state import env

env.user = 'mick'
env.hosts = ['93.170.123.27']


def deploy():
    with cd("projects/tealeaf-flask"):
        run("git pull")
        run("sudo restart tealeaf")
