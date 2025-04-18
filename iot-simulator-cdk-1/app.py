#!/usr/bin/env python3
import os

import aws_cdk as cdk
from aws_cdk import App, Environment
# Folder: iot_simulator_cdk_1
# File: iot_simulator_cdk_1/iot_simulator_cdk_1_stack.py
# Import the necessary class from the above file
from iot_simulator_cdk_1.iot_simulator_cdk_1_stack import IotSimulatorCdk1Stack

# account and region defined in the environment
env_aws =Environment(account='327625635979', region='eu-central-1')
'''
App is the main entry point for the CDK application.
App as the root: The App object is the entry point for defining your cloud infrastructure. It's the root construct of your CDK application, representing the entire deployment.

Construct tree: It acts as the base of the construct tree where all other resources (like stacks, constructs, etc.) are added. Every stack or resource you define must be attached to this app instance.

Synthesis: During the synthesis phase, cdk.App() generates the necessary CloudFormation templates based on the constructs defined in your application.
This is crucial for deploying your infrastructure as code, ensuring that your resources are created in a consistent and repeatable manner.
# Environment: The environment parameter allows you to specify the AWS account and region where the stack will be deployed. This is useful for multi-account or multi-region deployments.
'''
app = cdk.App()
#Stack definition, we can add many stacks here
s3_stack = IotSimulatorCdk1Stack(app, "IotSimulatorCdk1Stack", env=env_aws)
app.synth() 
'''
The synth() method is responsible for generating the CloudFormation templates based on the defined stacks and constructs. It translates your high-level CDK code into a low-level representation that AWS CloudFormation can understand.
Here, app.synth() generates the CloudFormation templates for the resources added under the App instance. It's the backbone of your CDK application!
The synth() method is called at the end of your CDK application to produce the CloudFormation templates that will be deployed to AWS.
The generated templates can be found in the cdk.out directory after running the application.
'''
