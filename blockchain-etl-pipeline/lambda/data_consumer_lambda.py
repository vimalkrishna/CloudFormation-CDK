import os
import boto3
import json
import logging
import base64
from decimal import Decimal
from datetime import datetime

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Get the DynamoDB table name from environment variables
TABLE_NAME = os.environ["DYNAMODB_TABLE_NAME"]

# Initialize DynamoDB resource and connect to the specified table
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

def handler(event, context):
    logger.info("Lambda function triggered")
    logger.info("Received event: %s", json.dumps(event))
    
    # DEBUG: Log table information
    try:
        table_info = table.meta.client.describe_table(TableName=TABLE_NAME)
        logger.info("DynamoDB Table Schema: %s", json.dumps(table_info['Table']['KeySchema']))
        logger.info("DynamoDB Table Attributes: %s", json.dumps(table_info['Table']['AttributeDefinitions']))
    except Exception as e:
        logger.error("Failed to get table info: %s", str(e))
    
    # Process each record from the Kinesis stream
    for i, record in enumerate(event["Records"]):
        try:
            logger.info(f"Processing record {i+1}/{len(event['Records'])}")
            
            # Decode and parse the base64-encoded Kinesis record
            payload = base64.b64decode(record["kinesis"]["data"])
            data = json.loads(payload.decode("utf-8"), parse_float=Decimal)
            
            logger.info("Original decoded record: %s", data)
            logger.info("Original record keys: %s", list(data.keys()))
            
            # Ensure necessary fields exist
            if "from_currency_code" not in data or "to_currency_code" not in data:
                logger.warning("Missing currency codes in record %d: %s", i+1, data)
                continue
            
            # Set partition key and sort key
            data["ticker"] = data["from_currency_code"] + data["to_currency_code"]
            data["timestamp"] = datetime.utcnow().isoformat()
            
            # DEBUG: Log the final data structure before insertion
            logger.info("Final data prepared for DynamoDB: %s", data)
            logger.info("Final data keys: %s", list(data.keys()))
            logger.info("Data types: %s", {k: type(v).__name__ for k, v in data.items()})
            
            # DEBUG: Check if timestamp field is actually present and not None/empty
            if "timestamp" not in data:
                logger.error("CRITICAL: timestamp key missing from data!")
            elif data["timestamp"] is None:
                logger.error("CRITICAL: timestamp value is None!")
            elif data["timestamp"] == "":
                logger.error("CRITICAL: timestamp value is empty string!")
            else:
                logger.info("Timestamp validation passed: %s (type: %s)", data["timestamp"], type(data["timestamp"]).__name__)
            
            # DEBUG: Validate all required keys before insertion
            required_keys = ["ticker", "timestamp"]  # Add other required keys based on your table schema
            missing_keys = [key for key in required_keys if key not in data or data[key] is None or data[key] == ""]
            
            if missing_keys:
                logger.error("Missing or empty required keys: %s", missing_keys)
                logger.error("Cannot insert record %d due to missing keys", i+1)
                continue
            
            logger.info("All required keys validated successfully")
            
            # Insert the processed data into the DynamoDB table
            logger.info("Attempting to insert item into DynamoDB...")
            response = table.put_item(Item=data)
            
            # DEBUG: Log the response from DynamoDB
            logger.info("DynamoDB put_item response: %s", response)
            logger.info("Successfully inserted record %d into DynamoDB", i+1)
            
        except json.JSONDecodeError as e:
            logger.error("JSON decode error for record %d: %s", i+1, str(e))
            logger.error("Raw payload: %s", payload)
        except Exception as e:
            logger.error("Error processing record %d: %s", i+1, str(e))
            logger.error("Record data at time of error: %s", data if 'data' in locals() else "No data available")
            
            # DEBUG: Log additional error context
            import traceback
            logger.error("Full traceback: %s", traceback.format_exc())
    
    return {
        'statusCode': 200,
        'body': json.dumps('Processing completed')
    }