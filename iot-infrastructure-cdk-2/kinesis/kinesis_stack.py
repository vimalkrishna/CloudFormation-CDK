#CDK resources we want to deploy
from aws_cdk import (
    Stack,
    aws_kinesis as kinesis,
    Duration,
    )

from constructs import Construct
from decouple import config

#get the environment variables, name of the stream
MY_STRESTREAM_NAME = config('VK_STREAM_NAME') 

# Create a Kinesis Class by extending Stack 

class KinesisStreamStack(Stack):
    """Creates a Kinesis stream with the specified name and retention period."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # Within init function, we define the resources we want to deploy, the kinesis stream
        
        my_kinesis_stream = kinesis.Stream(
            self,
            id="KinesisStream",
            stream_name=MY_STRESTREAM_NAME,
            shard_count=1, # create more shard for more throughput
            retention_period=Duration.hours(24), # set the retention period to 24 hours
            )
        


