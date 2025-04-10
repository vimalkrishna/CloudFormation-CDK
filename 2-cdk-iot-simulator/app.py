import aws_cdk as cdk
from aws_cdk import App, Environment

from cdk_iot_simulator_1.cdk_iot_simulator_1_stack import CdkIotSimulator1Stack

#Define account and region (Just change the region for multi-region   )
env_aws = Environment(account='327625635979', region='eu-central-1')

app = cdk.App()

#Stack definition, we can add many stacks here
s3_stack = CdkIotSimulator1Stack(app, "CdkIotSimulator1Stack",env=env_aws )

app.synth()
