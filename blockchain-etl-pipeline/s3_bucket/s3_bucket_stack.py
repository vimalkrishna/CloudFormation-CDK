from aws_cdk import Stack, aws_s3 as s3
from constructs import Construct
from decouple import config

# Get the S3 bucket name from environment variable
PRIMARY_BUCKET_NAME = config("PRIMARY_BUCKET_NAME", default="crypto-data-blockchain")
# 's3://crypto-data-blockchain/data/intradayCrypto' example location for the S3 bucket.
# We intend to copy data from DynamoDB for Spark ETL processing.

# Define the S3BucketStack class that inherits from AWS CDK Stack
class S3BucketStack(Stack): 
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        s3_bucket = s3.Bucket(self, id="PrimaryBucket", bucket_name=PRIMARY_BUCKET_NAME)
