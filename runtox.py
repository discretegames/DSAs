"""File to run tox since idk how to make launch.json do it directly."""

from subprocess import run

import os
print('DONE', run('tox -e py39'))
