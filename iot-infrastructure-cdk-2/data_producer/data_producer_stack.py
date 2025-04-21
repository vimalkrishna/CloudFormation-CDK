#CDK resources we want to deploy
from aws_cdk import (
    Stack,
    aws_kinesis as kinesis,
    Duration,
    aws_lambda  as _lambda,
    aws_events as events,
    aws_events_targets as targets,
    aws_s3 as s3,   
    aws_iam as iam,
    )

from constructs import Construct
from decouple import config

LAMBDA_RUNTIME = _lambda.Runtime.PYTHON_3_8
LAMBDA_PRODUCER_NAME = config('LAMBDA_PRODUCER_NAME')

 
# We need for global variable an environment. That is created for lambda runtime environment, to pass into stack.
ENVIRONMENT = {
    "API_KEY": config('API_KEY'),
    "VK_STREAM_NAME": config('VK_STREAM_NAME'),
}

class DataProducerStack(Stack):
    
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # Lambda function needs access to S3, Kinesis and CloudWatch
        
        lambda_role = iam.Role(
            self,
            id="LambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonKinesisFullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
            ]
        )
        
        

