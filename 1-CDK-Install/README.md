# We will make use of https://github.com/aws-samples/aws-cdk-examples
# This has tonns of great examples to try and implemment 

# CloudFormation-CDK
Install and setup.

# There must be npm installed
# We will need Docker installed for using Amazon Lambda Python Libraray
npm --version

# Installing CDK V2
npm install -g aws-cdk
# When using Window machine there will be UnauthorizedAccess exception when we test 
cdk --version
# In Window Machine power shell signed as administrator
Get-ExecutionPolicy  (Restricted)
Set-ExecutionPolicy RemoteSigned 
to Y

# PowerShell has several execution policies that control the conditions under which scripts can run:
Restricted:     No scripts can be run. This is the default setting.
AllSigned:      Only scripts signed by a trusted publisher can be run.
RemoteSigned:   Downloaded scripts must be signed by a trusted publisher, but locally written
                scripts can run without a signature.
Unrestricted:   All scripts can run, but a warning is shown for downloaded scripts.
Bypass:         All scripts can run without any restrictions or warnings.

# Good place to see working with Python with CDK 
https://docs.aws.amazon.com/cdk/v2/guide/work-with-cdk-python.html

# See the services on AWS
https://github.com/99designs/aws-vault/blob/master/USAGE.md

aws-vault securely stores and manages AWS credentials in development environments. It stores IAM credentials in your operating system's secure keystore and generates temporary credentials to expose to your shell and applications. 

