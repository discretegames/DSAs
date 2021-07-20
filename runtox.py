"""File to run tox since idk how to make launch.json do it directly."""

from subprocess import run

print('Running tox tests on Python 3.9 only...')
print('DONE', run('tox -e py39'))
