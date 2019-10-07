import os
import sys

from awslambda.logging import eprint


class CommandLineEventSource:

    def __init__(self):
        if len(sys.argv) > 2:
            self.event = sys.argv[2]
        else:
            eprint("docker-lambda.source.commandline.no-event")
            sys.exit(1)

    def poll(self):
        return self.event


class EnvironmentEventSource:

    def __init__(self):
        self.event = os.environ.get('AWS_LAMBDA_EVENT_BODY', {})
        if not self.event:
            eprint("docker-lambda.source.commandline.empty-event")

    def poll(self):
        return self.event
