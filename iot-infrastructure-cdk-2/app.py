#!/usr/bin/env python3
import os

import aws_cdk as cdk
from aws_cdk import Tags, Environment

from data_producer.data_producer_stack import DataProducerStack
from kinesis.kinesis_stack import KinesisStreamStack
# account and region defined in the environment
env_aws =Environment(account='327625635979', region='eu-central-1')

app = cdk.App()
# Tags for the whole stack
kinesis_stream = KinesisStreamStack(app, "KinesisStreamStack", env=env_aws)
data_producer = DataProducerStack(app, "DataProducerStack", env=env_aws)

Tags.of(app).add("ProjectOwner", "Vimal Krishna")

app.synth()
