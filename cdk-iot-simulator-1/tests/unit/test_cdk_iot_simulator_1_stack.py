import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_iot_simulator_1.cdk_iot_simulator_1_stack import CdkIotSimulator1Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_iot_simulator_1/cdk_iot_simulator_1_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkIotSimulator1Stack(app, "cdk-iot-simulator-1")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
