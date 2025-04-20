
# Welcome to another CDK Python project!

This is a major project for testing Kinesis with Lambda functions to receive IoT data from API, stream into kinesis using lambda function, then using another lambda function to consume it from kinesis stream, data anlytics (Apache Flink/Zepplin) on kinesis stream, transformation, ETL job(Glue) after saving into DynamoDB. The whole infrastruture is built using CDK(with Python).

```
$ tests
```

## Useful Informations about the project

 * `Alpha Vantage API`   Using free API from `https://www.alphavantage.co/`for cryptocurrency data feeds.    
 * `Data Producers      `First lambda function retrieves data from this API as Data producer for Kinesis    
 * `Data Consumers      `Second lambda function to fetch data from Kinesis stream and save to DB


