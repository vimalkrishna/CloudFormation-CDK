import aws_cdk as core
import aws_cdk.assertions as assertions

from 2_cdk_iot_simulator_1.2_cdk_iot_simulator_1_stack import 2CdkIotSimulator1Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in 2_cdk_iot_simulator_1/2_cdk_iot_simulator_1_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = 2CdkIotSimulator1Stack(app, "2-cdk-iot-simulator-1")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
