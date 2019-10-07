import os
import time

import boto3


class KinesisEventSource:
    """
    This class does a bare-bones simulation of the Lambda Kinesis event input to a Lambda function.

    It polls the Kinesis stream named by the environment variable ``KINESIS_STREAM_NAME`` once per second and returns
    any kinesis records found in the first shard as properly formatted Lambda Kinesis events following the example given
    here: https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis.html

    This will block until records are available, return all records found, then go back to waiting for records.

    Caveats:

        * We only poll the first shard in the stream
        * We don't do batching -- we return all available records

    If you define the environment variable ``KINESIS_ENDPOINT_URL``, we'll use that instead of the official AWS
    endpoint, allowing you to use kinesalite to simulate a Kinesis stream locally.
    """
    def __init__(self):
        self.stream_name = os.environ['KINESIS_self.stream_name']
        self.region = os.environ.get('AWS_REGION', os.environ.get('AWS_DEFAULT_REGION', 'us-east-1'))
        access_key_id = os.environ.get('AWS_ACCESS_KEY_ID', 'SOME_ACCESS_KEY_ID')
        secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY', 'SOME_SECRET_ACCESS_KEY')

        self.kinesis = boto3.client(
            'kinesis',
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=self.region,
            endpoint_url=os.environ.get('KINESIS_ENDPOINT_URL', None)
        )
        waiter = self.kinesis.get_waiter('stream_exists')
        waiter.wait(StreamName=self.stream_name)
        stream = self.kinesis.describe_stream(StreamName=self.stream_name)
        self.stream_arn = stream['StreamDescription']['StreamARN']
        shards = self.kinesis.list_shards(StreamName=self.stream_name)
        self.shard_id = shards['Shards'][0]['ShardId']
        self.shard_iterator = self.kinesis.get_shard_iterator(
            StreamName=self.stream_name,
            ShardId=self.shard_id
        )

    def poll(self):
        """
        This is what receive_invoke() calls.  This will block until records are available, return all records found and
        go back to waiting for records.
        """
        while 1:
            records = self.kinesis.get_records(ShardIterator=self.shard_iterator)
            if records:
                break
            # For standard iterators, Lambda polls each shard in your Kinesis stream for records at a base rate of once
            # per second.  When more records are available, Lambda keeps processing batches until it receives a batch
            # that's smaller than the configured maximum batch size. The function shares read throughput with other
            # consumers of the shard.
            # Ref: https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis.html
            time.sleep(1)

        events = {'Records': []}
        for krecord in records['Records']:
            events['Records'].append({
                "kinesis": {
                    "kinesisSchemaVersion": "1.0",
                    "partitionKey": "1",
                    "sequenceNumber": krecord['SequenceNumber'],
                    "data": krecord['Data'],
                    "approximateArrivalTimestamp": krecord['ApproximateArrivalTimestamp'].timestamp()
                },
                "eventSource": "aws:kinesis",
                "eventVersion": "1.0",
                "eventID": f"{self.shard_id}:{krecord['SequenceNumber']}",
                "eventName": "aws:kinesis:record",
                "invokeIdentityArn": "my_fake_arn",
                "awsRegion": self.region,
                "eventSourceARN": self.stream_arn
            })

        return events
