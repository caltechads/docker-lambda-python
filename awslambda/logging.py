from __future__ import print_function
import sys

orig_stdout = sys.stdout
orig_stderr = sys.stderr


def eprint(*args, **kwargs):
    print(*args, file=orig_stderr, **kwargs)
