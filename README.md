# docker-lambda-python

This is a mock AWS Lambda python 3.6 runtime environment that you can use to develop python lambda functions locally.
The image is based on the on the python 3.6 environment from [lambci/docker-lambda](https://github.com/lambci/docker-lambda), but enhances
that environment with extra features to make local development easier.

Since this image is built on the`lambci/docker-lambda:python3.6`, it has all the same features as that image:

> A sandboxed environment that replicates the live AWS Lambda environment
> almost identically – including installed software and libraries, file
> structure and permissions, environment variables, context objects and
> behaviors – even the user and running process are the same.

## What we added

Here are the differences between this python 3.6 environment and the one from
[lambci/docker-lambda](https://github.com/lambci/lambci):

* Rudimentary [AWS Lambda Layers](https://docs.aws.amazon.com/en_pv/lambda/latest/dg/configuration-layers.html) support
* Simulates [event source mappings](https://docs.aws.amazon.com/en_pv/lambda/latest/dg/invocation-eventsourcemapping.html),
  so that you can present a series of events to your lambda function, as would
  happen in production.  Supported event sources: 
  * Present a folder full of files, one event per file at a rate of your choosing
  * Perpetually read events from AWS Kinesis (or
    [kinesalite](https://hub.docker.com/r/dlsniper/kinesalite/), an AWS Kinesis 
    emulator you can run locally)
  * Read an event from an environment variable
  * Read an event from the command line
* Approximates the quasi-persistence of the [AWS Lambda Execution Context](https://docs.aws.amazon.com/en_pv/lambda/latest/dg/running-lambda-code.html).
  If you define objects outside the function handler's function in AWS, they will
  persist throughout the series of events you present with your mock event
  source mapping
