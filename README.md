# docker-lamdda-python

This is a mock AWS Lambda python 3.6 environment that you can use to develop python lambda functions locally.
It is based on the python 3.6 environment from [lambci/lambci](https://github.com/lambci/lambci), but enhances
that environment with extra features.

Here are the differences between this python 3.6 environment and the one from
[lambci/lambci](https://github.com/lambci/lambci):

* Supports [AWS Lambda Layers](https://docs.aws.amazon.com/en_pv/lambda/latest/dg/configuration-layers.html)
* Simulates [event source mappings](https://docs.aws.amazon.com/en_pv/lambda/latest/dg/invocation-eventsourcemapping.html),
  so that you can present a series of events to your lambda function, as would
  happen in production.
* Approximates the quasi-persistence of the [AWS Lambda Execution Context](https://docs.aws.amazon.com/en_pv/lambda/latest/dg/running-lambda-code.html).
  If you define objects outside the function handler's function in AWS, it will
  persist throughout the series of events you present with your mock event
  source mapping

