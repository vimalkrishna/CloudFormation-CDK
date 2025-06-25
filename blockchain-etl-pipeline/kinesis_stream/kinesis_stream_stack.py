# set of CDK resources we can deploy 
from aws_cdk import Stack, aws_kinesis as kinesis, Duration
from constructs import Construct
from decouple import config
# get the environment variables STREAM_NAME
INTRADAY_STREAM_NAME = config("INTRADAY_STREAM_NAME")

# EXTEND THE STACK CLASS TO CREATE A KINESIS STREAM (coPilot generates this code)
class KinesisStreamStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Define a Kinesis stream
        self.intraday_stream = kinesis.Stream(
            self,
            "IntradayStream",
            stream_name=INTRADAY_STREAM_NAME,
            shard_count=1,
            retention_period=Duration.hours(24),
        )

