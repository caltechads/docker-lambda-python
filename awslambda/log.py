from __future__ import print_function
import os
import sys

orig_stdout = sys.stdout
orig_stderr = sys.stderr


def eprint(*args, **kwargs):
    print(*args, file=orig_stderr, **kwargs)


def log(*args, **kwargs):
    if os.environ.get('DOCKER_LAMBDA_PYTHON_DEBUG', 'False') == 'True':
        eprint(*args, **kwargs)
