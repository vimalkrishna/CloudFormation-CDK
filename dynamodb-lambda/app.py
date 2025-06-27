#!/usr/bin/env python3
import os

import aws_cdk as cdk
from aws_cdk import Tags
from dynamodb_lambda.dynamodb_lambda_stack import DynamodbLambdaStack


app = cdk.App()
DynamodbLambdaStack(app, "DynamodbLambdaStack",
    env = cdk.Environment(account="327625635979", region="eu-central-1")
    )
# kinesis_stream = KinesisStreamStack(app, "KinesisStreamStack", env=env_EU)
Tags.of(app).add("ProjectOwner", "vimal krishna")
Tags.of(app).add("ProjectName", "dynamodb-lambda")

app.synth()
