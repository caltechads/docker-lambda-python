import os
import sys

from .filesystem import FilesystemEventSource
from .kinesis import KinesisEventSource
from .static import EnvironmentEventSource, CommandLineEventSource
from .logging import eprint


class EventSourceFactory:

    @staticmethod
    def new():
        source = os.environ.get('EVENT_SOURCE', 'commandline')
        if source not in ['filesystem', 'kinesis', 'environment', 'commandline']:
            eprint('docker-lambda.source.unknown source=%s' % source)
            sys.exit(1)
        else:
            eprint('docker-lambda.source.selected source=%s' % source)
        if source == 'filesystem':
            source = FilesystemEventSource()
        elif source == 'kinesis':
            source = KinesisEventSource()
        elif source == 'environment':
            source = EnvironmentEventSource()
        elif source == 'commandline':
            source = CommandLineEventSource()
        return source
