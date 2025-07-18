import aws_cdk as core
import aws_cdk.assertions as assertions

from blockchain_etl_pipeline.blockchain_etl_pipeline_stack import BlockchainEtlPipelineStack

# example tests. To run these tests, uncomment this file along with the example
# resource in blockchain_etl_pipeline/blockchain_etl_pipeline_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = BlockchainEtlPipelineStack(app, "blockchain-etl-pipeline")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
