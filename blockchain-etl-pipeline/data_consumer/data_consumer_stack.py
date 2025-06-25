# set of CDK resources we can deploy 
from aws_cdk import (
    Stack, 
    aws_dynamodb as dynamodb_,
    aws_lambda as _lambda, 
    Duration,
    aws_iam as iam,
    aws_s3 as s3,
    aws_events as events,
    aws_events_targets as targets,
    aws_kinesis as kinesis,
    aws_lambda_event_sources,
   
)
from constructs import Construct
from decouple import config

#get the global variable
LAMBDA_RUNTIME = config("LAMBDA_RUNTIME", default="python3.9")
LAMBDA_CONSUMER_NAME = config("LAMBDA_CONSUMER_NAME")
DYNAMODB_TABLE_NAME = config("DYNAMODB_TABLE_NAME" , default="crypto-table-blockchain")
INTRADAY_STREAM_NAME = config("INTRADAY_STREAM_NAME")
#STREAM_ARN = config("STREAM_ARN")
STREAM_ARN="arn:aws:kinesis:eu-central-1:327625635979:stream/" + INTRADAY_STREAM_NAME


ENVIRONMENT = {
    "DYNAMODB_TABLE_NAME": DYNAMODB_TABLE_NAME,
}

#  DataConsumerStack is a CDK stack that deploys a Lambda function to consume data from a Kinesis stream
class DataConsumerStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # Create a DynamoDB table
        dynamodb_table = dynamodb_.Table(
            self, 
            "DynamoDBIntradayTable",
            table_name=DYNAMODB_TABLE_NAME,
            partition_key=dynamodb_.Attribute(
                name="ticker", 
                type=dynamodb_.AttributeType.STRING),
            sort_key=dynamodb_.Attribute(   
                name="timestamp", 
                type=dynamodb_.AttributeType.STRING),
                
           # billing_mode=dynamodb_.BillingMode.PAY_PER_REQUEST,
            
        )

  # Now we need IAM role for the Lambda consumer function after we create the DynamoDB table
        lambda_consumer_role = iam.Role(
            self,
            "LambdaConsumerRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonKinesisFullAccess"),
                # This policy allows the Lambda function to access DynamoDB
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AmazonDynamoDBFullAccess"
                ),
            ],
        )
# after role is created, we can create the Lambda handler  function
# Create the Lambda function for data consumption
        crypto_data_consumer = _lambda.Function(
            self,
            "DataConsumerHandler",
            function_name=LAMBDA_CONSUMER_NAME,
            runtime=_lambda.Runtime.PYTHON_3_8,
            #runtime=LAMBDA_RUNTIME,
            code=_lambda.Code.from_asset("lambda"),
            timeout=Duration.seconds(20),
            handler="data_consumer_lambda.handler",
            environment=ENVIRONMENT,
            role=lambda_consumer_role,
        )

        # We need to create trigger, that any time data is written to kinesis, it gets triggered. Kinesis stream using its ARN is needed bring in the resource.
        stream = kinesis.Stream.from_stream_arn(
            self, "IntradayStream", stream_arn=STREAM_ARN
        )

# Get event handler, then add Kinesis stream event source.
# LATEST and TRIM_HORIZON are the two options for starting position.
# https://docs.aws.amazon.com/kinesis/latest/APIReference/API_StartingPosition.html
        crypto_data_consumer.add_event_source(
            aws_lambda_event_sources.KinesisEventSource(
                stream,
                batch_size=100,
                starting_position=_lambda.StartingPosition.LATEST,
            )
        )
