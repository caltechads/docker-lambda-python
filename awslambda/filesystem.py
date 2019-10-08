import os
import sys
import time

from awslambda.log import eprint, log


class FilesystemEventSource:
    """
    This class does a truly bare-bones simulation of an event stream input to a Lambda function.

    Given a folder full of events recorded from a lambda function (one event per file, saved as JSON), iterate over the
    those files and present the events to the lambda function with a period given by FILESYSTEM_SLEEP_SECONDS
    (default: 1).  Once the last file has been presented, loop around to the first file and start again.
    """

    def __init__(self):
        self.folder_name = os.environ['FILESYSTEM_FOLDER']
        self.period = int(os.environ.get('FILESYSTEM_SLEEP_SECONDS', 1))
        self.loop = os.environ.get('FILESYSTEM_LOOP', "False") == "True"
        # Either "exit" or "wait"
        self.exit_policy = os.environ.get('FILESYSTEM_EXIT_POLICY', "exit")
        self.files = [
            os.path.join(self.folder_name, f)
            for f in os.listdir(self.folder_name)
            if os.path.isfile(os.path.join(self.folder_name, f))
        ]
        self.files.sort()
        self.index = 0
        log("docker-lambda.source.filesystem.start folder=%s files=%s loop=%s period=%s" % (
            self.folder_name,
            len(self.files),
            self.loop,
            self.period
        ))
        self.is_done = False

    def poll(self):
        if len(self.files) > 0:
            if self.index < len(self.files):
                with open(self.files[self.index], 'r') as fd:
                    events = fd.read()
                log("docker-lambda.source.filesystem.done.event-loaded folder=%s file=%s" % (
                    self.folder_name,
                    self.files[self.index]
                ))
                self.index += 1
                if self.index >= len(self.files):
                    if self.loop:
                        self.index = 0
                        log("docker-lambda.source.filesystem.done.rewind folder=%s loop=%s" % (
                            self.folder_name,
                            self.loop
                        ))
                    else:
                        log(
                            "docker-lambda.source.filesystem.done.no-more-files "
                            "folder=%s loop=%s exit-policy=%s" % (
                                self.folder_name,
                                self.loop,
                                self.exit_policy
                            )
                        )
                        if self.exit_policy == "wait":
                            while True:
                                time.sleep(30)
                        else:
                            log("docker-lambda.source.filesystem.done")
                            self.is_done = True
        else:
            eprint("docker-lambda.source.filesystem.error.no-files folder=%s" % self.folder_name)
            sys.exit(1)
        time.sleep(self.period)
        return events

    def done(self):
        return self.is_done
