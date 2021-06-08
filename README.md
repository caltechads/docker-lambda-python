# docker-lambda-python

This is a mock AWS Lambda python 3.6 runtime environment that you can use to
develop python lambda functions locally.  The image is based on the on the
python 3.6 environment from
[lambci/docker-lambda](https://github.com/lambci/docker-lambda), but enhances
that environment with extra features to make local development easier.

Since this image is built on the`lambci/docker-lambda:python3.6`, it has
similar features as that image.  It a sandboxed environment that mostly replicates
the live AWS Lambda environment – including installed software and libraries,
file structure and permissions, environment variables, context objects and
behaviors – even the user and running process are the same.

## Notable differences from the actual AWS Lambda environment

* We have `boto3` and its dependencies installed into `/var/runtime`.  This is
  not necessarily true in the AWS environment.

## Available image tags in Docker Hub

 * `caltechads/docker-python-lambda:python3.6`: the latest version of the image
 * `caltechads/docker-python-lambda:python3.6-build5`: the specific tag of latest version of the
   image.  Use this is you want to pin to a specific build of
   `caltechads/docker-lambda-python:python:3.6

## What we added

Here are the differences between this python 3.6 environment and the one from
[lambci/docker-lambda](https://github.com/lambci/lambci):

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

## Running docker-lambda-python

You can run your Lambdas from local directories using the `-v` arg with `docker run` 
– logging goes to stderr and the callback result goes to stdout.

You mount your (unzipped) lambda code at `/var/task` and any (unzipped) layer
code at `/opt`, and most runtimes take two arguments – the first for the handler
and the second for the event, ie:

```
# With a lambda module named my_module.py containing a handler function
docker run --rm -v "$PWD":/var/task lambci/lambda:python3.6 my_module.handler

# With a lambda module named my_module.py containing a handler function and a layer
# in $PWD/layer
docker run --rm -b "$PWD"/layer:/opt -v "$PWD":/var/task lambci/lambda:python3.6 my_module.handler
```


## Debugging docker-lambda-python

To make docker-lambda-python itself log to stderr so that you can see what it
is doing, define the `DOCKER_LAMBDA_PYTHON_DEBUG` environment variable to be "True":

```
# With a lambda module named my_module.py containing a handler function
docker run --rm -e "DOCKER_LAMBDA_PYTHON_DEBUG=True" -v "$PWD":/var/task lambci/lambda:python3.6 my_module.handler
```
