import os
import sys

from awslambda.log import log


class CommandLineEventSource:

    def __init__(self):
        self.is_done = False

    def poll(self):
        if len(sys.argv) > 2:
            event = sys.argv[2]
        else:
            log("docker-lambda.source.commandline.no-event")
            event = "{}"
        self.is_done = True
        return event

    def done(self):
        if self.is_done:
            log("docker-lambda.source.commandline.done")
        return self.is_done


class EnvironmentEventSource:

    def __init__(self):
        self.is_done = False

    def poll(self):
        event = os.environ.get('AWS_LAMBDA_EVENT_BODY', {})
        if not event:
            log("docker-lambda.source.environment.no-event")
        self.is_done = True
        return event

    def done(self):
        if self.is_done:
            log("docker-lambda.source.environment.done")
        return self.is_done
