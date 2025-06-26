# Implementing Real-Time Analytics in Blockchain Application.
Visibility is very important in any real-time applications. In distributed application, it becomes critical. The goal of this application is to store streaming data, and create different types of data pipelines including ETL using AWS CDK. Once IaC is created, it can be used in any CI/CD pipeline. AWS CodePipeline is the preferred way as AWS managed services will be used here.

Companion blog on this topic: [Implementing ETL pipeline with CDK](
 https://aws-cloud-deployment.blogspot.com/2025/06/implementing-etl-pipeline-with-cdk.html)

 In this serverless stack created with AWS CDK, the data producer component fetches the data from (DOGECoin, Bitcoin, and Ethereum conversion rate to USD) from Alpha Vantage API, and pushes into Kinesis. From kinesis, another serverless component, data consumer fetches data and puts into DynamoDB. After having data in kinesis, we can implement different possiblites for visualisation /integration needs. 


## Technical stack details
1.  Python 3.8
2.  Alpha Vantage API
3.  CloudWatch
4.  DynamoDb
5.  S3
6.  Athena
7.  Apache Flink / Apache Zeppelin
8.  AWs Glue/Spark
9.  AWS CDK
10. Lambda serverless 
11. VSCode
12. miniconda


## Key components created
1. data_consumer_stack
2. data_producer_stack
3. kinesis_stream_stack
4. s3_bucket_stack


![Arch diagram](img/ETL-PipelineSVG.drawio.svg)



## Basic deployment steps
1. Fetch alpha vantage [API key](https://www.alphavantage.co/support/#api-key)
2. Clone (get) the git application.

I have used monorepo for CDK project. It needs a Git Subdirectory Checkout for the developers. This is called sparse checkout.

`git clone --filter=blob:none --no-checkout https://github.com/vimalkrishna/CloudFormation-CDK.git`

`cd CloudFormation-CDK`

`git sparse-checkout init --cone`

`git sparse-checkout set blockchain-etl-pipeline`

You can get Code as ZIP of the parent folder will all subprojects.
Alternatively (best option) you can use use Github service called https://download-directory.github.io/ and paste the link 
https://github.com/vimalkrishna/CloudFormation-CDK/tree/main/blockchain-etl-pipeline

   Setup the AWS CLI with your account and credentials.

   Also setup CDK by installing Node.js, the AWS CDK CLI, and configure your AWS credentials. See the official AWS website.
   
   Open the downloaded project in editor like VSCode, create .env file in the root folder, inside blockchain-etl-pipeline with the following contents.

###  Add .env file to gitignore to avoid committing the following sensitive information
    
```
    INTRADAY_STREAM_NAME=kinesis-crypto-intraday
    API_KEY=YOURKEY # 25 calls per day only 
    (Producer calls every 2 minutes)
    LAMBDA_RUNTIME=python3.8
    LAMBDA_PRODUCER_NAME=crypto-data-producer
    LAMBDA_CONSUMER_NAME=crypto-data-consumer
    DYNAMODB_TABLE_NAME=crypto-table-blockchain
    PRIMARY_BUCKET_NAME=crypto-data-blockchain
```
3. cdk bootstrap
4. cdk synth (Test all stacks)
5. cdk deploy
    - cdk deploy kinesis_stream_stack 
    - cdk deploy data_consumer_stack
    - cdk deploy data_producer_stack
    - cdk deploy s3_bucket_stack

6. Manually, create system using AWS console to use Apache flink,  Athena, and Zeppline. These extension I will add later in a blog as there are visual editors to be used.




