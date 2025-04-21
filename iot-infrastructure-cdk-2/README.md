
# Welcome to another CDK Python project!

My goal was to learn about REAL-Time data handling by using some key AWS technology like Kinesis, Lambda functions, and using Analytics on those data. At first we will use alphavantage API to get live data for currency. In future projects, reflect that understanding for massive amount of data eminating from IOT sensors coming to Kinesis, with more shards and increasing the complexities for different usecases.

To receive IoT/streaming data, stream into kinesis using lambda function, then using another lambda function to consume it from kinesis stream, for data anlytics (Apache Flink/Zepplin) on kinesis stream, transformation, ETL job(Glue) after saving into DynamoDB. The whole infrastruture is being built using CDK(with Python).
All implementations can be improved! 
Codes have been annotated to give some more understanding for a new comer on python world (like me!)

Put your own free API key in .env file in project root
```
VK_STREAM_NAME= iot_kinesis_stream
API_KEY = XXXXXXXXXXXX
LAMBDA_PRODUCER_NAME = iot_kinesis_producer
LAMBDA_CONSUMER_NAME = iot_kinesis_consumer	
```

Concept of layer is important, a library to be used across multiple lambda functions. 
Panda for DataScience works, parquet layers like wise alphavantage layer here.
We need to call alphavantage

I am using older python version as at many places the version was causing problem, i was unbale to move forward.
Also used wsl as 20 giga RAM on laptop was proving to be insufficient.
```
(.venv) (aws) vimal@LAPTOP-Vimal:~/AWS-Works/CloudFormation-CDK/iot-infrastructure-cdk-2$ python3 --version
Python 3.8.10
(.venv) (aws) vimal@LAPTOP-Vimal:~/AWS-Works/CloudFormation-CDK/iot-infrastructure-cdk-2$ cdk --version
2.175.1 (build afe6e87)
```


## Useful Informations about the project

 * `Alpha Vantage API`   Using free API from `https://www.alphavantage.co/`for currency data feeds.    
 


