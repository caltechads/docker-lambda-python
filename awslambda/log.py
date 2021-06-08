from __future__ import print_function
import os
import sys

ORIG_STDOUT = sys.stdout
ORIG_STDERR = sys.stderr


def eprint(*args, **kwargs):
    print(*args, file=ORIG_STDERR, **kwargs)


def log(*args, **kwargs):
    if os.environ.get('DOCKER_LAMBDA_PYTHON_DEBUG', 'False') == 'True':
        eprint(*args, **kwargs)
