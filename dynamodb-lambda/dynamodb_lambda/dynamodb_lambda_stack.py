from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    RemovalPolicy,
    Duration
)
from constructs import Construct

class DynamodbLambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create DynamoDB Table
        self.users_table = dynamodb.Table(
            self, "UsersTable",
            table_name="users-learning-table",
            partition_key=dynamodb.Attribute(
                name="user_id", 
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="timestamp", 
                type=dynamodb.AttributeType.STRING
            ),
            # For learning purposes, allow easy cleanup
            removal_policy=RemovalPolicy.DESTROY,
            # Enable point-in-time recovery (good practice)
            point_in_time_recovery=True,
            # Billing mode - on-demand for learning (no capacity planning needed)
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )

        # Add Global Secondary Index for querying by email
        self.users_table.add_global_secondary_index(
            index_name="email-index",
            partition_key=dynamodb.Attribute(
                name="email",
                type=dynamodb.AttributeType.STRING
            ),
            # No sort key for this GSI - allows simple email lookups
        )

        # Lambda function for basic CRUD operations
        self.crud_lambda = _lambda.Function(
            self, "DynamoDbCrudLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="crud_handler.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
            timeout=Duration.seconds(30),
            environment={
                "TABLE_NAME": self.users_table.table_name
            }
        )

        # Lambda function for batch operations
        self.batch_lambda = _lambda.Function(
            self, "DynamoDbBatchLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="batch_handler.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
            timeout=Duration.seconds(30),
            environment={
                "TABLE_NAME": self.users_table.table_name
            }
        )

        # Lambda function for query operations
        self.query_lambda = _lambda.Function(
            self, "DynamoDbQueryLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="query_handler.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
            timeout=Duration.seconds(30),
            environment={
                "TABLE_NAME": self.users_table.table_name
            }
        )

        # Grant permissions to Lambda functions
        self.users_table.grant_full_access(self.crud_lambda)
        self.users_table.grant_full_access(self.batch_lambda)
        self.users_table.grant_full_access(self.query_lambda)

        # Create API Gateway for testing
        api = apigateway.RestApi(
            self, "DynamoDbLearningApi",
            rest_api_name="DynamoDB Learning API",
            description="API for learning DynamoDB operations"
        )

        # CRUD endpoints
        users_resource = api.root.add_resource("users")
        users_resource.add_method("POST", apigateway.LambdaIntegration(self.crud_lambda))  # Create user
        users_resource.add_method("GET", apigateway.LambdaIntegration(self.crud_lambda))   # List users
        
        user_resource = users_resource.add_resource("{user_id}")
        user_resource.add_method("GET", apigateway.LambdaIntegration(self.crud_lambda))    # Get user
        user_resource.add_method("PUT", apigateway.LambdaIntegration(self.crud_lambda))    # Update user
        user_resource.add_method("DELETE", apigateway.LambdaIntegration(self.crud_lambda)) # Delete user

        # Batch operations endpoint
        batch_resource = api.root.add_resource("batch")
        batch_resource.add_method("POST", apigateway.LambdaIntegration(self.batch_lambda))

        # Query operations endpoint
        query_resource = api.root.add_resource("query")
        query_resource.add_method("GET", apigateway.LambdaIntegration(self.query_lambda)
        )