"""File to run targeted tox tests."""

from subprocess import run

print('Running tox tests on Python 3.9 only...')
print('DONE', run('tox -e py39'))
