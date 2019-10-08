import os
import sys

from .filesystem import FilesystemEventSource
from .kinesis import KinesisEventSource
from .static import EnvironmentEventSource, CommandLineEventSource
from .logging import eprint


class EventSourceFactory:

    @staticmethod
    def new():
        """
        Select our event input based on the `EVENT_SOURCE` environment variable setting.  `EVENT_SOURCE` can currently
        have one of a these settings:

            * ``commandline``: accept a single event as a string on the `docker` command line
            * ``environment``: Read a single event from the `AWS_LAMBDA_EVENT_BODY` environment variable
            * ``filesystem``: Read one or more events from a folder in the Docker filesystem; either built
               in to the image or mounted through a volume mount
            * ``kinesis``: read events from a Kinesis stream, or from a kinesalite stream

        :rtype: an event source class
        """
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
