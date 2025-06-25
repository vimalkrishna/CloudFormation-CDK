# set of CDK resources we can deploy 
from aws_cdk import (
    Stack, 
    aws_lambda as _lambda, 
    Duration,
    aws_iam as iam,
    aws_s3 as s3,
    aws_events as events,
    aws_events_targets as targets,
)
from constructs import Construct
from decouple import config

#get the global variable
LAMBDA_RUNTIME = config("LAMBDA_RUNTIME", default="python3.9")
LAMBDA_PRODUCER_NAME = config("LAMBDA_PRODUCER_NAME")

ENVIRONMENT = {
    "API_KEY": config("API_KEY"),
    "INTRADAY_STREAM_NAME": config("INTRADAY_STREAM_NAME"),
}
# Define the tuple of crypto conversions to be processed
CRYPTO_CONVERSIONS = [("BTC", "USD"), ("ETC", "USD"), ("DOGE", "USD")]
# These are Bitcon, Ethereum and Dogecoin conversions to USD.


# EXTEND THE STACK CLASS TO CREATE A KINESIS STREAM (coPilot generates this code)
class DataProducerStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_role = iam.Role(  
            self, 
            "LambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonKinesisFullAccess"),
            ],
        )
        
# we need to create LAYER, from a that is in Layers/Alpha-vantage/python folder 
# After pipe install -t . alpha_vantage, we need a Lambda functions 
        alpha_vantage_layer = _lambda.LayerVersion(
            self,
            "AlphaVantageLayer",
            code=_lambda.AssetCode("Layers/alpha_vantage_layer"),
            #compatible_runtimes=[_lambda.Runtime.from_string(LAMBDA_RUNTIME)],
        )

# Now we create the Lambda function that will fetch crypto data using the Alpha Vantage API.
        crypto_data_producer = _lambda.Function(
            self,
            "CryptoDataHandler",
            function_name=LAMBDA_PRODUCER_NAME,
            #runtime=LAMBDA_RUNTIME,
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset("lambda"),# code resides in lambda folder
            timeout=Duration.seconds(60),
            layers=[alpha_vantage_layer], # Associates previously defined Lambda layer.
            handler="data_producer_lambda.handler",
            environment=ENVIRONMENT, # Passes a dictionary of environment variables to the Lambda.
            role=lambda_role, #Associates the IAM role to grants  necessary permissions.
        )
# Now we need to schedule lambda execution using EventBridge scheduled rule (every minute)
        intraday_rule = events.Rule(
            self, 
            "IntradayRule", 
            schedule=events.Schedule.rate(Duration.minutes(2))
        )
# We are looking 3 crypto currency conversions from BTC, ETC and DOGE to USD.
# Add Lambda function as a target for each crypto conversion, interating through tuple CRYPTO_CONVERSIONS
        for conversion in CRYPTO_CONVERSIONS:
            intraday_target = targets.LambdaFunction(
                crypto_data_producer,
                event=events.RuleTargetInput.from_object(
                    {"from_currency": conversion[0], "to_currency": conversion[1]}
                ),
            )
            intraday_rule.add_target(intraday_target)
#Each target is added to the EventBridge rule with add_target, ensuring that every invocation includes the right parameters.