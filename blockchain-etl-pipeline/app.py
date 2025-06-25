#!/usr/bin/env python3
import os
import aws_cdk as cdk
from aws_cdk import Tags


from kinesis_stream.kinesis_stream_stack import KinesisStreamStack
from data_producer.data_producer_stack import DataProducerStack
from data_consumer.data_consumer_stack import DataConsumerStack
from s3_bucket.s3_bucket_stack import S3BucketStack

# Using env_EU ensures all stacks—like Kinesis Stream, Data Producer, Data Consumer, # and S3 Bucket—are instantiated in eu-central-1. 
# This is crucial for maintaining a structured cloud infrastructure. 
env_EU = cdk.Environment(account="327625635979", region="eu-central-1")


app = cdk.App()

kinesis_stream = KinesisStreamStack(app, "KinesisStreamStack", env=env_EU)
data_producer = DataProducerStack(app, "DataProducerStack", env=env_EU)
data_consumer = DataConsumerStack(app, "DataConsumerStack", env=env_EU)
s3_bucket = S3BucketStack(app, "S3BucketStack", env=env_EU)

# All stacks deployed under this CDK app will inherit these tags,
# making cloud resource management, cost allocation & billing and monitoring more efficient when many people are spining resources. There are much more benefits to tagging resources.
Tags.of(app).add("ProjectOwner", "vimal krishna")
Tags.of(app).add("ProjectName", "blockchain-etl-pipeline")

app.synth()